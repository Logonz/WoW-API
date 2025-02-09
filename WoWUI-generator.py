#!/usr/bin/env python3
import os
import argparse
import shutil


def parse_toc_file(toc_path):
  """
  Reads a .toc file and returns a set of allowed file paths.
  Ignores header lines (starting with '##') and blank lines.
  Each file entry is normalized (and Windows-style backslashes are converted).
  """
  allowed = set()
  try:
    with open(toc_path, "r", encoding="utf-8") as f:
      for line in f:
        stripped = line.strip()
        if not stripped or stripped.startswith("##"):
          continue
        normalized = os.path.normpath(stripped.replace("\\", os.sep))
        allowed.add(normalized)
  except Exception as e:
    print(f"Error reading {toc_path}: {e}")
  return allowed


unfold_folders = ["shared", "wrath", "tbc", "cata", "classic", "vanilla"]


def adjust_file_entry(entry, version, addon_name):
  """
  Checks whether the file entry has an extra (redundant) folder level corresponding
  to the version. For example, if entry is:

      Classic/Blizzard_AchievementUI.lua

  and version is "Classic" (and addon_name is "Blizzard_AchievementUI"),
  then remove the third folder so that the result becomes:

      Blizzard_AchievementUI.lua

  If the expected pattern is not detected, return the entry unchanged.
  """
  parts = entry.split(os.sep)
  # Look for the pattern:
  # parts[0] == version, parts[1] == addon_name, and parts[2] == version.
  if len(parts) >= 2:
    if parts[0].lower() in unfold_folders:
      new_entry = os.sep.join(parts[1:])
      print(f"    Adjusted file entry: {entry} -> {new_entry}")
      return new_entry
  return entry


def process_addon_directory(addon_dir, version, source_addons_root, dest_addons_root):
  """
  For a given addon folder, select the appropriate base and version-specific TOC files,
  then:
    - Parse the base TOC to obtain allowed file entries.
    - Read the version-specific TOC, filtering out any file entry not in the allowed set.
    - Recreate the addon's folder under dest_addons_root.
    - Copy all files referenced (with relative paths preserved), except any .toc files.

  The function looks for a TOC file ending with _{version}.toc.
  It also attempts to pick a genuine base TOC (one that does not look version-specific)
  to use for allowed entries. If no such base exists but the version TOC exists, the
  version TOC is used for both roles.
  """
  # List all .toc files in the addon folder.
  toc_files = [f for f in os.listdir(addon_dir) if f.lower().endswith(".toc")]
  if not toc_files:
    return

  base_toc = None
  version_toc = None
  # Define known version tags (if a TOC file ends with _<tag>.toc, it is considered version-specific).
  known_tags = {"Cata", "TBC", "Vanilla", "Wrath", "Classic"}

  for toc in toc_files:
    # If the file name ends with _{version}.toc, mark it as the version-specific TOC.
    if toc.endswith(f"_{version}.toc"):
      version_toc = toc
      continue

    # Otherwise, if the file appears version-specific (its name contains an underscore with a known tag)
    if "_" in toc:
      parts = toc.rsplit("_", 1)
      if len(parts) == 2:
        tag = parts[1].rsplit(".", 1)[0]
        if tag in known_tags:
          # This TOC file is marked for some version; skip it as a base.
          continue
        else:
          base_toc = toc
      else:
        base_toc = toc
    else:
      # If there is no underscore, use it as a base.
      base_toc = toc

  # If no genuine base TOC was found but a version-specific TOC exists,
  # use the version-specific TOC as the base.
  if base_toc is None and version_toc is not None:
    base_toc = version_toc

  if version_toc is None:
    print(f"Version TOC file for version '{version}' not found in {addon_dir}. Skipping this addon.")
    return

  base_toc_path = os.path.join(addon_dir, base_toc)
  version_toc_path = os.path.join(addon_dir, version_toc)

  print(f"\nProcessing addon in folder: {addon_dir}")
  print(f"  Base TOC: {base_toc}")
  print(f"  Version TOC: {version_toc}")

  allowed_entries = parse_toc_file(base_toc_path)
  if not allowed_entries:
    print(f"  No allowed file entries found in base TOC {base_toc_path}. Skipping this addon.")
    return

  # Process the version-specific TOC file: filter out file entries not in the allowed set.
  # (We still use its contents to determine what files to copy.)
  filtered_lines = []
  file_entries = []  # normalized file paths that will be copied
  try:
    with open(version_toc_path, "r", encoding="utf-8") as f:
      lines = f.readlines()
    for line in lines:
      stripped = line.strip()
      if not stripped or stripped.startswith("##"):
        filtered_lines.append(line)
      else:
        normalized = os.path.normpath(stripped.replace("\\", os.sep))
        if normalized in allowed_entries:
          filtered_lines.append(line)
          file_entries.append(normalized)
        else:
          print(f"  Skipping file entry '{stripped}' in {version_toc_path} (not found in base TOC).")
  except Exception as e:
    print(f"Error processing {version_toc_path}: {e}")
    return

  # Determine the addon folder's relative path (relative to the source addons root)
  rel_addon_dir = os.path.relpath(addon_dir, source_addons_root)
  dest_addon_dir = os.path.join(dest_addons_root, rel_addon_dir)
  os.makedirs(dest_addon_dir, exist_ok=True)

  # Do not write out the .toc file; we only copy non-.toc files referenced in the filtered TOC.
  # When copying, adjust the destination path if an extra version folder is detected.
  addon_name = os.path.basename(addon_dir)
  for entry in file_entries:
    if entry.lower().endswith(".toc"):
      print(f"    Skipping .toc file: {entry}")
      continue
    # Adjust the entry if it contains an extra version folder.
    adjusted_entry = adjust_file_entry(entry, version, addon_name)
    src_file = os.path.join(addon_dir, entry)
    dest_file = os.path.join(dest_addon_dir, adjusted_entry)
    if os.path.exists(src_file):
      os.makedirs(os.path.dirname(dest_file), exist_ok=True)
      try:
        shutil.copy2(src_file, dest_file)
        print(f"    Copied: {src_file} -> {dest_file}")
      except Exception as e:
        print(f"    Error copying {src_file} to {dest_file}: {e}")
    else:
      print(f"    Source file {src_file} does not exist; skipping copy.")


def copy_annotations():
  """
  Copies all folders from './vscode-wow-api/Annotations/*' to './API/*'.
  """
  src_annotations = os.path.join(".", "vscode-wow-api", "Annotations")
  dest_api = os.path.join(".", "API")
  if not os.path.isdir(src_annotations):
    print(f"Annotations source folder {src_annotations} not found.")
    return
  for item in os.listdir(src_annotations):
    src_item = os.path.join(src_annotations, item)
    dest_item = os.path.join(dest_api, item)
    if os.path.isdir(src_item):
      try:
        shutil.copytree(src_item, dest_item, dirs_exist_ok=True)
        print(f"Copied annotations folder: {src_item} -> {dest_item}")
      except Exception as e:
        print(f"Error copying annotations folder {src_item} to {dest_item}: {e}")


def main():
  parser = argparse.ArgumentParser(
    description="Recreate a copy of the WoWUI folder structure containing only files "
    "referenced by the version-specific TOC files (excluding .toc files). "
    "You can supply one or more versions. If 'Classic' is chosen, 'Vanilla' is automatically added."
  )
  parser.add_argument("--version", required=True, help="Version suffix (e.g. Wrath)")
  args = parser.parse_args()
  version = args.version

  versions = [version]

  # Normalize version names using a mapping.
  mapping = {"wrath": "Wrath", "tbc": "TBC", "cata": "Cata", "classic": "Classic", "vanilla": "Vanilla"}
  versions = [mapping.get(v.lower(), v) for v in versions]

  # If 'Classic' is one of the versions and 'Vanilla' isn't explicitly specified, add it.
  if "Classic" in versions and "Vanilla" not in versions:
    versions.append("Vanilla")

  print(f"Processing versions: {', '.join(versions)}")

  # Define the source AddOns folder.
  source_addons_root = os.path.join(".", "WoWUI", "Interface", "AddOns")
  if not os.path.isdir(source_addons_root):
    print(f"Source AddOns folder not found at {source_addons_root}")
    return

  # For each version, create a destination folder under API/<Version> and process each addon.
  for version in versions:
    dest_addons_root = os.path.join(".", "API", "UI")
    print(f"\n=== Processing destination for version '{version}' at {dest_addons_root} ===")
    for addon in os.listdir(source_addons_root):
      addon_dir = os.path.join(source_addons_root, addon)
      if os.path.isdir(addon_dir):
        process_addon_directory(addon_dir, version, source_addons_root, dest_addons_root)

  # --- New post-processing steps ---
  print("\n--- Post-processing API folders ---")
  copy_annotations()

  # Rename the API folder to the version from args.version
  print(f"\nRenaming API folder to API-{args.version}")
  dest_api = os.path.join(".", "API")
  dest_version = os.path.join(".", f"API-{args.version}")

  if os.path.isdir(dest_version):
    print(f"Destination folder {dest_version} already exists. Removing directory.")
    shutil.rmtree(dest_version)

  os.rename(dest_api, dest_version)

  # Check if Functions-Classic-AI folder exists
  print("\nChecking if Functions-Classic-AI folder exists")
  dest_functions = os.path.join(".", "Functions-Classic-AI")
  if os.path.isdir(dest_functions):
    # Copy the folder into the API folder
    print("Copying Functions-Classic-AI folder into API folder")
    dest = os.path.join(dest_version, "Functions-AI")
    shutil.copytree(dest_functions, dest, dirs_exist_ok=True)


if __name__ == "__main__":
  main()

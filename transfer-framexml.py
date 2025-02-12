import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Only run this block for Gemini Developer API
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

with open("LuaTypes.md", "r") as f:  # changed variable from os to f
  LuaTypesContent = f.read()

model = "gemini-2.0-flash-lite-preview-02-05"
# model = "gemini-2.0-flash"


def add_type_hint(source: str, type_hint_multiline: str, anchor_line: str) -> str:
  # Split the source string into lines
  lines = source.split("\n")

  # Find the index of the line that contains the anchor
  anchor_line_index = next((i for i, line in enumerate(lines) if anchor_line in line), None)

  # If the anchor is not found, return the original source
  if anchor_line_index is None:
    return source

  # Insert the type hint above the anchor line
  new_lines = lines[:anchor_line_index] + [type_hint_multiline] + lines[anchor_line_index:]

  # Join the list of lines back into a single string
  return "\n".join(new_lines)


def Add_Function_Hint(source: str, anchor_line: str, type_hint_multiline: str) -> str:
  print("Add_Function_Hint", anchor_line, type_hint_multiline)
  return add_type_hint(source, type_hint_multiline, anchor_line)


def Add_Table_Hint(source: str, anchor_line: str, type_hint_multiline: str) -> str:
  print("Add_Table_Hint", anchor_line, type_hint_multiline)
  return add_type_hint(source, type_hint_multiline, anchor_line)


def Done_Adding_Type_Hints() -> None:
  print("Done adding type hints.")
  pass


add_function_hint_def = types.FunctionDeclaration(
  name="Add_Function_Hint",
  description="""Add all type hints above an anchor line, for example: 'function name(param1)'
Use \\n between each line of the type hint but not at the end.
# Example 1:

default_api.Add_Function_Hint(anchor_line = "function ExtractLinkData(link)", type_hint_multiline = "--- Extracts the link data from a link.\\n---[FrameXML](https://www.townlong-yak.com/framexml/go/ExtractLinkData)\\n---@param link string\\n---@return string? linkType\\n---@return string? linkData")

# Example 2:

default_api.Add_Function_Hint(anchor_line = "function BNGetInfo()", type_hint_multiline = "--- Returns the player's own Battle.net info.\\n---[Documentation](https://warcraft.wiki.gg/wiki/API_BNGetInfo)\\n---@return number? presenceID\\n---@return string battleTag\\n---@return number toonID\\n---@return string currentBroadcast\\n---@return boolean bnetAFK\\n---@return boolean bnetDND\\n---@return boolean isRIDEnabled")

NEVER include the anchor line in the type hint.""",
  parameters=types.Schema(
    type="OBJECT",
    properties={
      "type_hint_multiline": types.Schema(type="STRING"),
      "anchor_line": types.Schema(type="STRING"),
    },
    required=["type_hint_multiline", "anchor_line"],
  ),
)

add_table_hint_def = types.FunctionDeclaration(
  name="Add_Table_Hint",
  description="""Add all table type hints above an anchor line, for example: 'LinkMixin = {{}}'
Use \\n between each line of the type hint but not at the end.
# Example 1:

default_api.Add_Table_Hint(anchor_line = "LinkMixin = {{}};", type_hint_multiline = "---[FrameXML](https://www.townlong-yak.com/framexml/go/LinkMixin)\\n---@class LinkMixin : LinkType")

# Example 2:

default_api.Add_Table_Hint(anchor_line = "LinkMixin = {{}}", type_hint_multiline = "---[FrameXML](https://www.townlong-yak.com/framexml/go/LinkMixin)\\n---@class LinkMixin")

NEVER include the anchor line in the table type hint.""",
  parameters=types.Schema(
    type="OBJECT",
    properties={
      "type_hint_multiline": types.Schema(type="STRING"),
      "anchor_line": types.Schema(type="STRING"),
    },
    required=["type_hint_multiline", "anchor_line"],
  ),
)

done_adding_type_hints_def = types.FunctionDeclaration(
  name="Done_Adding_Type_Hints", description="When all available dynamic_meta_information has been added to the source code, call this function."
)


def Transfer_info(meta_info: str, source: str, destination: str):
  """
  Transfer the meta information to the source code.
  So the idea behind this is to use the meta information from
   - vscode-wow-api/Annotations/Interface/Blizzard_SharedXML/Color.lua or similar
  and add it to the source code in
    - WoWUI/Interface/AddOns/Blizzard_SharedXML/Color.lua or similar

  Because clicking the information in vscode jumps to the meta information files because the source code does not have the meta information.
  You can get to the sourcecode by doing jump to implementation in vscode.
  """

  system_prompt = f"""Your job is to read the meta information type hint about a function and then add the type hint to the function in the source code and use Done_Adding_Type_Hints when you are done.

# Documentation
{LuaTypesContent}

<dynamic_meta_information>
{meta_info}
</dynamic_meta_information>


1. Add type hint summary
2. Add documentation url
  a. Example: [FrameXML](https://www.townlong-yak.com/framexml/go/ExtractLinkData)
  b. Example: [Documentation](https://warcraft.wiki.gg/wiki/API_BNGetInfo)
3. Add parameter type hints, if any
4. Add return type hint, if any"""

  tool = types.Tool(function_declarations=[add_function_hint_def, add_table_hint_def, done_adding_type_hints_def])

  response = client.models.generate_content(
    model=model,
    # This pure also works, the extra is a second test that was last used.
    # contents=content,
    contents=f"# Source:\n{source}\n Never include the anchor_line in the type_hint_multiline.",
    config=types.GenerateContentConfig(
      # This pure also works, the extra is a second test that was last used.
      # Remember to ermove the <functions> from the system_instruction if you are using the pure contents.
      # system_instruction=system_prompt,
      system_instruction=system_prompt,
      temperature=0,
      tools=[tool],
    ),
  )

  source = source

  for func in response.function_calls:
    if func.name == "Add_Function_Hint":
      source = Add_Function_Hint(source, func.args["anchor_line"], func.args["type_hint_multiline"])
    elif func.name == "Add_Table_Hint":
      source = Add_Table_Hint(source, func.args["anchor_line"], func.args["type_hint_multiline"])
    elif func.name == "Done_Adding_Type_Hints":
      Done_Adding_Type_Hints()

  with open(destination, "w") as f:
    f.write(source)


# vscode-wow-api/Annotations/Interface/Blizzard_SharedXML/Color.lua
# WoWUI/Interface/AddOns/Blizzard_SharedXML/Color.lua


if __name__ == "__main__":
  with open("./vscode-wow-api/Annotations/Interface/Blizzard_SharedXML/Color.lua", "r") as f:
    meta_info = f.read()
  with open("./WoWUI/Interface/AddOns/Blizzard_SharedXML/Color.lua", "r") as f:
    source = f.read()

  Transfer_info(meta_info, source, "./Color.lua")

LUA Type Annotations

Add context to code and type checking.

Annotations prefixed with `---`, like Lua comment with extra dash.

Annotation Formatting

Annotations support markdown syntax: headings, bold text, italic text, struckthrough text, ordered list, unordered list, blockquote, code, code block, horizontal rule, link, image.

Add newlines to annotations: extra line of `---`, HTML `<br>` tag (recommended), `\n`, two trailing spaces, Markdown backslash `\` (not recommended).

```lua
---@alias MyCustomType integer

---Calculate a value using [my custom type](lua://MyCustomType)
function calculate(x) end
```

Tips
Type `---` above a function for suggested snippet with `@param` and `@return` annotations.

Documenting Types
Documenting types with language server is important. Recognized Lua types: `nil`, `any`, `boolean`, `string`, `number`, `integer`, `function`, `table`, `thread`, `userdata`, `lightuserdata`.

Simulate classes and fields, create own types. Adding `?` after type like `boolean?` means `boolean|nil`.

Advanced types documentation:

Type | Document As:
--- | ---
Union Type | `TYPE_1 \| TYPE_2`
Array | `VALUE_TYPE[]`
Tuple | `[VALUE_TYPE, VALUE_TYPE]`
Dictionary | `{ [string]: VALUE_TYPE }`
Key-Value Table | `table<KEY_TYPE, VALUE_TYPE>`
Table literal | `{ key1: VALUE_TYPE, key2: VALUE_TYPE }`
Function | `fun(PARAM: TYPE): RETURN_TYPE`

Unions may need parentheses in certain situations:

```Lua
---@type (string | integer)[]
local myArray = {}
```

Understanding This Page
To understand annotations, know how to read Syntax sections.

Symbol | Meaning
--- | ---
`<value_name>` | Required value
`[value_name]` | Optional
`[value_name...]` | Repeatable
`value_name | value_name` | Left or right side valid
Other symbols are syntactically required.

Annotations List
Annotations recognized by language server:

@alias
Create own type or enum.

Syntax
`---@alias <name> <type>`

Examples
Simple alias

```Lua
---@alias userID integer The ID of a user
```

Custom Type

```Lua
---@alias modes "r" | "w"
```

Custom Type with Descriptions

```Lua
---@alias DeviceSide
---| '"left"' # The left side
---| '"right"' # The right side
---| '"top"' # The top side
---| '"bottom"' # The bottom side
---| '"front"' # The front side
---| '"back"' # The back side

---@param side DeviceSide
local function checkSide(side) end
```

Literal Custom Type

```Lua
local A = "Hello"
local B = "World"

---@alias myLiteralAlias `A` | `B`

---@param x myLiteralAlias
function foo(x) end
```

@as
Force a type onto an expression.
Warning: Cannot be added using `---@as <type>`, must be done like `--[[@as <type>]]`.

Syntax
`--[[@as <type>]]`

Examples
Override Type

```Lua
---@param key string Must be a string
local function doSomething(key) end

local x = nil

doSomething(x --[[@as string]])
```

@async
Mark a function as asynchronous. When hint.await is true, functions marked with @async will have an await hint displayed.

Syntax
`---@async`

Examples
Mark Function Async

```Lua
---@async
---Perform an asynchronous HTTP GET request
function http.get(url) end
```

@cast
Cast a variable to a different type or types.

Syntax
`---@cast <value_name> [+|-]<type|?>[, [+|-]<type|?>...]`

Examples
Simple Cast

```Lua
---@type integer | string
local x

---@cast x string
print(x) --> x: string
```

Add Type

```Lua
---@type integer
local x

---@cast x +boolean
print(x) --> x: integer | boolean
```

Remove Type

```Lua
---@type integer|string
local x

---@cast x -integer
print(x) --> x: string
```

Cast Multiple Types

```Lua
---@type string
local x --> x: string

---@cast x +boolean, +number
print(x) --> x:string | boolean | number
```

Cast Possibly `nil`

```Lua
---@type string
local x

---@cast x +?
print(x) --> x:string?
```

@class
Define a class. Can be used with @field to define a table structure. A class can inherit one or more parent classes.

Syntax
`---@class [(exact)] <name>[: <parent>[, <parent>...]]`

Examples
Define a Class

```Lua
---@class Car
local Car = {}
```

Class Inheritance

```Lua
---@class Vehicle
local Vehicle = {}

---@class Plane: Vehicle
local Plane = {}
```

Create exact class

```Lua
---@class (exact) Point
---@field x number
---@field y number
local Point = {}
Point.x = 1 -- OK
Point.y = 2 -- OK
Point.z = 3 -- Warning
```

How the table Class is Implemented

```Lua
---@class table<K, V>: { [K]: V }
```

@enum
Mark a Lua table as an enum.

Syntax
`---@enum [(key)] <name>`

Examples
Define Table as Enum

```Lua
---@enum colors
local COLORS = {
  black = 0,
  red = 2,
  green = 4,
  yellow = 8,
  blue = 16,
  white = 32
}

---@param color colors
local function setColor(color) end

setColor(COLORS.green)
```

Define Table Keys as Enum

```Lua
---@enum (key) Direction
local direction = {
    LEFT = 1,
    RIGHT = 2,
}

---@param dir Direction
local function move(dir)
    assert(dir == "LEFT" or dir == "RIGHT")

    assert(direction[dir] == 1 or direction[dir] == 2)
    assert(direction[dir] == direction.LEFT or direction[dir] == direction.RIGHT)
end

move("LEFT")
```

@field
Define a field within a table. Should be immediately following a @class.

Syntax
`---@field [scope] <name[?]> <type> [description]`

Examples
Simple Documentation of a Class

```Lua
---@class Person
---@field height number The height in cm
---@field weight number The weight in kg
---@field firstName string The first name
---@field lastName? string The last name
---@field age integer The age

---@param person Person
local function hire(person) end
```

Mark Field as Private

```Lua
---@class Animal
---@field private legs integer
---@field eyes integer

---@class Dog:Animal
local myDog = {}

---Child class Dog CANNOT use private field legs
function myDog:legCount()
  return self.legs
end
```

Mark Field as Protected

```Lua
---@class Animal
---@field protected legs integer
---@field eyes integer

---@class Dog:Animal
local myDog = {}

---Child class Dog can use protected field legs
function myDog:legCount()
  return self.legs
end
```

Typed Field

```Lua
---@class Numbers
---@field named string
---@field [string] integer
local Numbers = {}
```

@generic
Generics allow code reuse and serve as a "placeholder" for a type.

Syntax
`---@generic <name> [:parent_type] [, <name> [:parent_type]]`

Examples
Generic Function

```Lua
---@generic T : integer
---@param p1 T
---@return T, T[]
function Generic(p1) end

-- v1: string
-- v2: string[]
local v1, v2 = Generic("String")

-- v3: integer
-- v4: integer[]
local v3, v4 = Generic(10)
```

Capture with Backticks

```Lua
---@class Vehicle
local Vehicle = {}
function Vehicle:drive() end

---@generic T
---@param class `T` # the type is captured using `T`
---@return T       # generic type is returned
local function new(class) end

-- obj: Vehicle
local obj = new("Vehicle")
```

Array Class Using Generics

```Lua
---@class Array<T>: { [integer]: T }

---@type Array<string>
local arr = {}

-- Warns that I am assigning a boolean to a string
arr[1] = false

arr[3] = "Correct"
```

Dictionary Class Using Generics

```Lua
---@class Dictionary<T>: { [string]: T }

---@type Dictionary<boolean>
local dict = {}

-- no warning despite assigning a string
dict["foo"] = "bar?"

dict["correct"] = true
```

@meta
Marks a file as "meta", used for definitions, not functional Lua code.

Syntax
`---@meta [name]`

Examples
Mark Meta File

```Lua
---@meta [name]
```

@module
Simulates require-ing a file.

Syntax
`---@module '<module_name>'`

Examples
"Require" a File

```Lua
---@module 'http'

--The above provides the same as
require 'http'
--within the language server
```

"Require" a File and Assign to a Variable

```Lua
---@module 'http'
local http

--The above provides the same as
local http = require 'http'
--within the language server
```

@nodiscard
Mark a function as having return values that cannot be ignored. A warning will be raised if returns are not captured.

Syntax
`---@nodiscard`

Examples
Prevent Ignoring a Function's Returns

```Lua
---@return string username
---@nodiscard
function getUsername() end
```

@operator
Provides type declarations for an operator metamethod.
Syntax
`---@operator <operation>[(param_type)]:<return_type>`

Examples
Declare `__add` Metamethod

```Lua
---@class Vector
---@operator add(Vector): Vector

---@type Vector
local v1
---@type Vector
local v2

--> v3: Vector
local v3 = v1 + v2
```

Declare Unary Minus Metamethod

```Lua
---@class Passcode
---@operator unm:integer

---@type Passcode
local pA

local pB = -pA
--> integer
```

Declare `__call` Metamethod

```Lua
---@class URL
---@operator call:string
local URL = {}
```

@overload
Define an additional signature for a function.
Syntax
`---@overload fun([param: type[, param: type...]]): [return_value[,return_value]]`

Examples
Define Function Overload

```Lua
---@param objectID integer The id of the object to remove
---@param whenOutOfView boolean Only remove when not visible
---@return boolean success If successfully removed
---@overload fun(objectID: integer): boolean
local function removeObject(objectID, whenOutOfView) end
```

Define Class Call Signature

```Lua
---@overload fun(a: string): boolean
local foo = setmetatable({}, {
  __call = function(a)
    print(a)
        return true
  end,
})

local bool = foo("myString")
```

@package

Mark a function as private to the file. Cannot be accessed from another file.

Syntax

`---@package`

Examples

Mark a Function as Private to a Package

```Lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@package
---Cannot be accessed in another file
function Animal:eyesCount()
    return self.eyes
end
```

@param
Define a parameter for a function. This helps enforce types and provide completion. A question mark (`?`) after the name marks it as optional.
Syntax
`---@param <name[?]> <type[|type...]> [description]`

Examples
Simple Function Parameter

```Lua
---@param username string The name to set for this user
function setUsername(username) end
```

Parameter Union Type

```Lua
---@param setting string The name of the setting
---@param value string|number|boolean The value of the setting
local function settings.set(setting, value) end
```

Optional Parameter

```Lua
---@param role string The name of the role
---@param isActive? boolean If the role is active
---@return Role
function Role.new(role, isActive) end
```

Variable Number of Parameters

```Lua
---@param index integer
---@param ... string Tags to add to this entry
local function addTags(index, ...) end
```

Generic Function Parameter

```Lua
---@class Box

---@generic T
---@param objectID integer The ID to set the type of
---@param type `T` The type to set
---@return `T` object The object as a Lua object
local function setObjectType(objectID, type) end

--> boxObject: Box
local boxObject = setObjectType(1, "Box")
```

Custom Type Parameter

```Lua
---@param mode string
---|"'immediate'"  # comment 1
---|"'async'" # comment 2
function bar(mode) end
```

Literal Custom Type Parameter

```Lua
local A = 0
local B = 1

---@param active integer
---| `A` # Has a value of 0
---| `B` # Has a value of 1
function set(active) end
```

@private

Mark a function as private to a class. Accessible only from within class.

Syntax

`---@private`

Examples

Mark a function as private

```Lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@private
function Animal:eyesCount()
    return self.eyes
end

---@class Dog:Animal
local myDog = {}

---NOT PERMITTED!
myDog:eyesCount();
```

@protected

Mark a function as protected within a class. Accessible from within class or child classes.

Syntax

`---@protected`

Examples

Mark a function as protected

```Lua
---@class Animal
---@field private eyes integer
local Animal = {}

---@protected
function Animal:eyesCount()
    return self.eyes
end

---@class Dog:Animal
local myDog = {}

---Permitted because function is protected, not private.
myDog:eyesCount();
```

@return

Define a return value for a function. This helps enforce types and provide completion.

Syntax

`---@return <type> [<name> [comment] | [name] #<comment>]`

Examples

Simple Function Return

```Lua
---@return boolean
local function isEnabled() end
```

Named Function Return

```Lua
---@return boolean enabled
local function isEnabled() end
```

Named, Described Function Return

```Lua
---@return boolean enabled If the item is enabled
local function isEnabled() end
```

Described Function Return

```Lua
---@return boolean # If the item is enabled
local function isEnabled() end
```

Optional Function Return

```Lua
---@return boolean|nil error
local function makeRequest() end
```

Variable Function Returns

```Lua
---@return integer count Number of nicknames found
---@return string ...
local function getNicknames() end
```

@type

Mark a variable as a certain type. Union types separated with `|`.

Syntax

`---@type <type>`

Examples

Basic Type Definition

```Lua
---@type boolean
local x
```

Array Type Definition

```Lua
---@type string[]
local names
```

Dictionary Type Definition

```Lua
---@type { [string]: boolean }
local statuses
```

Table Type Definition

```Lua
---@type table<userID, Player>
local players
```

Union Type Definition

```Lua
---@type boolean|number|"yes"|"no"
local x
```

Function Type Definition

```Lua
---@type fun(name: string, value: any): boolean
local x
```

@vararg

Mark a function as having variable arguments. For variable returns, see @return.

This annotation has been deprecated and is for legacy support for EmmyLua annotations. Use @param instead.

Syntax

`---@vararg <type>`

Examples

Basic Variable Function Arguments

```Lua
---@vararg string
function concat(...) end
```

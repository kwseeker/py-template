# Pydantic

Pydantic 是使用最广泛的 Python 数据校验库。

Pydantic [功能和优势](https://docs.pydantic.dev/latest/#why-use-pydantic)。

Pydantic [使用说明文档](https://docs.pydantic.dev/latest/concepts/models/)。

使用流程：

1. 定义模型类并将字段定义为带注解的属性

	模型是继承 BaseModel 的类，校验逻辑都是通过这个基类实现的。
	还可以使用`根模型（RootModel）`或 `TypeAdapter` 实现对基本类型的校验逻辑。

	```python
	user_list_adapter = TypeAdapter(list[User]) 
	user_list = user_list_adapter.validate_python([{'name': 'Fred', 'id': '3'}])
	```

	在定义字段校验逻辑时，可以使用 `Field()` 提供更丰富的校验功能（默认值、字段别名、数值约束、字符串约束、十进制约束、数据类约束、严格模式等等），其行为与标准库 `field()` 函数用于数据类的方式相同。
	支持两种使用方式：
	
	```python
	# 但是注意这种方式会产生误导，参考官方文档
	class Model(BaseModel): 
		name: str = Field(..., frozen=True)

	class Model(BaseModel): 
		name: Annotated[str, Field(strict=True), WithJsonSchema({'extra': 'data'})]
	```

	还可以通过 `ConfigDict` 控制模型校验行为，可以通过 `model_config` 属性或类参数设置模型配置，也可以通过 Pydantic dataclasses 装饰器 `@dataclass` 为数据类设置模型配置。
	`TypeAdapter` 也支持 `ConfigDict` 配置（通过 `config` 参数设置）。
	可以通过定义父模型类全局修改所有子模型类的校验行为，因为配置是可以被继承的。

	```python
	class Model(BaseModel): 
		model_config = ConfigDict(str_max_length=5)
		v: str
	
	class Model(BaseModel, frozen=True): 
		a: str

	@dataclass(config=ConfigDict(str_max_length=10, validate_assignment=True)) 
	class User: 
		name: str
	```

	另外还可以通过实现[校验器(Validators)](https://docs.pydantic.dev/latest/concepts/validators/)，自定义校验逻辑细节。

2. 执行校验

	Pydantic 在**执行模型对象初始化（__init__）时会自动执行校验**，另外模型提供了一些校验方法（类方法）可以校验字典、JSON数据是否符合模型约束，比如 `model_validate()`、`model_validate_json()`。
	有时在创建模型对象时可能不希望执行校验，可以使用 `model_cosntruct()` 创建模型对象。

3. 错误处理

	Pydantic 在验证数据时发现任何错误，都会引发 `ValidationError` 异常，一个异常中包含所有发现的校验错误。

除了类型校验，还支持以下功能：

+ 数据转换

	将输入数据强制转换为符合模型字段类型的对象。
	严格模式下允许的类型转换表：[Conversion Table](https://docs.pydantic.dev/latest/concepts/conversion_table/)。

	默认情况下，Pydantic 会尝试在可能的情况下将值转换为期望的类型。例如，你可以将字符串 `"123"` 作为 `int` 字段的输入，它将被转换为 `123` 。
	然而，也有一些情况下不希望这样做，而希望 Pydantic 在数据不正确时报错而不是进行转换。为了更好地支持这种用例，Pydantic 提供了一种“严格模式”，可以在模型级别、字段级别，甚至每次验证调用时启用。当启用严格模式时，Pydantic 在转换数据时会变得不那么宽容，如果数据类型不正确，则会报错。

+ 额外数据处理

	可以对模型约束之外的数据采取 `ignore`（默认行为）、`forbid`、`allow`（额外数据存储在 `__pydantic_extra__` 字典属性中，可以通过显示的注解提供对额外字段的验证） 处理。

+ 嵌套模型
+ 泛型模型
+ 动态模型

	使用运行时信息来指定字段创建模型，比如 `DynamicFoobarModel = create_model('DynamicFoobarModel', foo=str, bar=(int, 123))` 相当于定义了：

	```python
	class StaticFoobarModel(BaseModel): 
		foo: str 
		bar: int = 123
	```

+ 根类型

	RootModel 是专门为那些只需要包含单个字段（即“根字段”）的数据结构而设计的模型类型。它允许你为非对象结构（如基本类型、列表、字典等）创建一个更正式的数据模型。与 `BaseModel` 类似，但它只包含一个字段。

	```python
	Pets = RootModel[list[str]]
	print(Pets(['dog', 'cat']))
	print(Pets.model_validate(['dog', 'cat']))
	```

+ TypeAdapter

	可以直接验证一个对象是否符合某个类型结构，而**不需要定义一个完整的 Pydantic 模型类**。它是对基本类型（如 `str`, `int`, `list`, `dict`）的增强，使其具备数据验证和解析能力。

+ 伪不可变性

	即禁止修改实例属性的值。可以通过 `model_config['frozen'] = True` 配置模型为不可变。

+ 校验装饰器（Validation Decorator）

	提供 `validate_call()` 装饰器允许在调用函数之前，使用函数的注解来解析和验证传递给函数的参数。
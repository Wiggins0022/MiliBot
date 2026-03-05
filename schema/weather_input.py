from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city_name: str = Field(
        ...,
        description="必须且只能提取出纯粹的城市中文名，剔除所有时间词（如明天）、疑问词（如怎么样）、名词后缀（如市、天气）。例如输入'明天郑州天气'，只能输出'郑州'。"
    )
    relative_day: str = Field(
        default="今天",
        description="用户想要查询的时间。必须且只能从以下四个词中选一个：'今天'、'明天'、'后天'、'大后天'。如果没有明确说明，默认填'今天'。"
    )
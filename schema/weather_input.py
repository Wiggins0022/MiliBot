from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    city_name: str = Field(
        ...,
        description="必须且只能提取出纯粹的城市中文名，剔除所有时间词（如明天）、疑问词（如怎么样）、名词后缀（如市、天气）。例如输入'明天郑州天气'，只能输出'郑州'。"
    )
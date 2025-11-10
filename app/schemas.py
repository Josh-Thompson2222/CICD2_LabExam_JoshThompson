from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict

NameStr = Annotated[str, StringConstraints(min_length = 1, max_length = 100)]
EmailStr = 
CustomerSinceInt = Annotated[int, Ge(2000), Le[2100]]
OrderNumberInt = Annotated[int, Constraints(min_length = 3, max_length = 20)]
TotalCentsInt = Annotated[int, Constraints(min_length = 1, max_length = 1000000)]


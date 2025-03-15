from pydantic import BaseModel, Field

class Book(BaseModel):
    id: int = Field(..., gt=0, description="O ID deve ser maior que 0")
    title: str = Field(..., min_length=1, max_length=100, description="O título deve ter entre 1 e 100 caracteres")
    author: str = Field(..., min_length=1, max_length=100, description="O nome do autor deve ter entre 1 e 100 caracteres")
    year: int = Field(..., gt=0, description="O ano deve ser um número inteiro positivo")
    genre: str = Field(..., min_length=1, max_length=50, description="O gênero deve ter entre 1 e 50 caracteres")
    pages: int = Field(..., gt=0, description="O número de páginas deve ser um número inteiro positivo")
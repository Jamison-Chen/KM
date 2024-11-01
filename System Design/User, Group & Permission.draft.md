### Model 1

```mermaid
erDiagram
    User }o--o{ Group: contains
    Group }o--o{ Permissions: has
    Permissions }o--o{ User: has
```

#TODO 

# Battle Board
Created by Emmett Tackaberry for Computer Science course

## How to Play
1. Download *start.py*, *main.py*, *enemy.py*, and *text.py* from Github repository
2. Move scripts into new folder
3. Run start.py

## Game Information
**Battle Board** is a text-based video game made with Python. You play against an enemy AI on a 6x6 board where you can either move your own squadron or attack an enemy squadron with the squadrons you chose prior to playing. 
**Battle Board** includes a difficulty selector with the difficulties *Easy*, *Normal*, *Hard*, and *Impossible*, each with varying attributes. The enemy AI is based on a basic iterative deepening minimax algorithm with alpha-beta pruning.

### Squadron Information
|Squadron|Health|Attack range|Move range|Damage|Bonus damage|Bonus against|
|--------|------|------------|----------|------|------------|-------------|
|Archer  |100   |4           |1         |95    |30          |Spearman     |
|Footman |350   |1           |2         |85    |10          |Archer       |
|Spearman|650   |1           |1         |50    |100         |Cavalier     |
|Cavalier|500   |1           |3         |90    |30          |Mage         |
|Mage    |200   |3           |2         |70    |40          |Footman      |

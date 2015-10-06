To run the code:
python MDP.py [worldfile.txt] [epsilon value]

After confirming that the program runs correctly and provides an optimal solution, I ran the test with multiple epsilon values. 
First, I decrimented epsilon to smaller values, however this resulted in no effect in the output. 
Next, I began increasing the epsilon value by 0.5 each run. This also resulted in no variance in the output.
However, once the epsilon value grew greater than 3, the outputted path changed, and it began giving suboptimal routes, such as going through mountainous regeons where it could have continued through open areas. 
By increasing the epsilon value, we are allowing the equation to end while performing fewer calculations, which results in a less accurate estimate. Therefore, the higher the epsilon given, the fewer calculations occur, and the less refined the value becomes. 
Therefore, it is better to have a significantly small epsilon in order to refine the value to an accurate number. 

TicTacToe Environment in Eclipse
================================

1. Copy all files contained in the zip-Archive to a new directory 
   in your Eclipse workspace, e.g. "workspace/TicTacToe". 

2. Create a new Java-Project in Eclipse that has the same name as the 
   directory you just created, e.g. "TicTacToe". 
   (see screenshot eclipse1.png)

3. Make sure that all *.jar files contained in the "lib" directory are 
   listed as "referenced libraries" (see left side of screenshot 
   eclipse2.png). If the are not listed as referenced libraries, open 
   the project's properties, and add each jar file to the "build path".
   (see eclipse3.png)

4. Eclipse should be able to compile NewPlayer.java. You can now start 
   programming.

5. In order to play a match or tournament in Eclipse, you first need 
   to add the "config" directory, to the projects class path 
   (eclipse6.png). Make sure that this entry is located above the 
   project itself (eclipse7.png), otherwise your modifications to the 
   configuration files will not have any effect.

   Finally, create a new RunConfiguration (eclipse2.png) called 
   "Java-Application" (eclipse4.png) and add the class 
   "de.ovgu.dke.teaching.ml.tictactoe.PlayMatch" as main class 
   (eclipse5.png). Press "Run" and your first match should start.
   
   In order to play a tournament, simply choose 
   "de.ovgu.dke.teaching.ml.tictactoe.PlayTournament" as main class.

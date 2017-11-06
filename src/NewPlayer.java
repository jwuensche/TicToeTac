import java.util.Arrays;

import de.ovgu.dke.teaching.ml.tictactoe.api.IBoard;
import de.ovgu.dke.teaching.ml.tictactoe.api.IMove;
import de.ovgu.dke.teaching.ml.tictactoe.api.IPlayer;
import de.ovgu.dke.teaching.ml.tictactoe.api.IllegalMoveException;
import de.ovgu.dke.teaching.ml.tictactoe.game.Move;
import de.ovgu.dke.teaching.ml.tictactoe.util.Indexing;

/**
 * 
 * @author Marten Wallewein-Eising, Johann Wagner, Johannes Wuensche, Paul Stang
 */

public class NewPlayer implements IPlayer {
	//float w0, w1, w2, w3, w4;
	float learningRate = 0.001f;
	int moves =0;
	int matches =0;
	int lost=0;
	/**
	 * Backup of implementation in https://github.com/jwuensche/TicToeTac/commit/a9d015965f726a3761f8bcf3622fa80b2153da36
	 */
	float[] weights = {0, 1, 1, 1, 1 };
	
	public NewPlayer(){
		
	}
	
	public String getName() {
		// TODO Auto-generated method stub
		return "TicToeTac";
	}


	public int[] makeMove(IBoard board)
	{	
		// create a clone of the board that can be modified
		moves++;
		int[] currentParams = new int[board.getDimensions()];
		IMove bestMove = new Move(this, new int[] {1, 0,0});
		float bestScore = Integer.MIN_VALUE, currentScore = 0;
		
		do
		{
			IBoard copy = board.clone();
			if(board.getFieldValue(currentParams) != null)
				continue;
			
			// do a move using the cloned board
			try {
				
				Move currentMove = new Move(this, currentParams.clone());
				copy.makeMove(currentMove);
				
				currentScore = classifyBoard(copy);
				if(currentScore > bestScore)
				{
					bestMove = currentMove;
					bestScore = currentScore;
				}
					
			} catch (IllegalMoveException e) {
				// move was not allowed
			}
			
		}
		while(Indexing.incrementIndices(currentParams, board.getSize()));
		
		return bestMove.getPosition();
	}
	
	/**
	 *  Least mean square error algorithm learning the weights based on the given error
	 * @param boardPrev Last board state
	 * @param boardAft Current board state
	 */
	private void LMS(IBoard boardPrev, IBoard boardAft)
	{
		float moveValue = this.classifyMove(boardPrev, boardAft);
		LMS(boardAft, moveValue);
	}
	
	/**
	 * Least mean square error algorithm learning the weights based on the given error
	 * @param board Current Board state
	 * @param error Training error, @see documentation
	 */
	private void LMS(IBoard board, float error){
		int[] params = this.getParameters(board);

		for(int i = 0; i < params.length; ++i)
		{
			this.weights[i] = this.weights[i] + this.learningRate * params[i] * error;
		}
	}
	
	/**
	 * Calculates the difference of the board scores of the last and current board
	 * @param boardPrev Last board state
	 * @param boardAft Current board state@param boardPrev
	 * @return Score difference
	 */
	private float classifyMove(IBoard boardPrev, IBoard boardAft){
		return this.classifyBoard(boardAft) - this.classifyBoard(boardPrev);
	}
	
	/**
	 * Calculates the Board score based on the current weights
	 * @param board Current Board state
	 * @return Board score
	 */
	private float classifyBoard(IBoard board){
		
		int [] params = this.getParameters(board);
		float sum = 0;
		for(int i = 0; i < params.length; ++i)
		{
			sum += this.weights[i] * params[i];
		}
		
		return sum;
		//return this.w0 + this.w1 * param[0] + this.w2 * param[1] + this.w3 * param[2] + this.w4 * param[3];
		
	}
	/**
	 * Returns the Score parameters which are used for LMS
	 * Definition of parameters:
	 * x0: 1
	 * x1: Count of own rows, which can be completed
	 * x2: Count of enemy rows, which can be completed
	 * x3: Count of min marks required to fill a row
	 * x4: Count of min enemy marks required to fill a row
	 * @param board
	 * @return int[] of x0, ..., xi
	 */
	private int[] getParameters(IBoard board){
		int[] index1 = {0,0,0};
		int[] index2 = {0,0,0};
		int[] param = {0,0,0,board.getSize(), board.getSize()};
		//Notation for already seen players on a row
		IPlayer[] rows =new IPlayer[board.getSize()]; 
		int layers = 1;
		if(board.getDimensions() > 2)
			layers = board.getSize();
		
		//Begin search structure
		while (layers > 0){
		layers--;
		index1[2] = index2[2] = layers;
		for(int column = 0; column < board.getSize(); column++){
			index1[0] = column;
			//Notation for already seen Player in a column
			IPlayer columns = null;
			int marks = board.getSize();

			for(int row = 0; row < board.getSize(); row++){
				index1[1] = row;
				//Check for occupation
				if(board.getFieldValue(index1) != null && columns == null)
					columns = board.getFieldValue(index1);
				//Check for occupation conflict
				else if(board.getFieldValue(index1) != null && columns != board.getFieldValue(index1))
					break;
				//Check for occupation continuation
				else if(board.getFieldValue(index1) != null && columns == board.getFieldValue(index1))
					marks--;
				//Check for end
				if(row == board.getSize() - 1){
					if(this != columns && columns != null){
						param[2]++;
						if(marks < param[4])
							param[4] = marks;
					}
					else if(this == columns){
						param[1]++;
						if(marks < param[3])
							param[3] = marks;
					}
				}
			}
			// ------ end column search
		}

		for(int row = 0; row < board.getSize(); row++){
			index2[1] = row;
			//Notation for already seen Player in a column
			IPlayer columns = null;
			int marks = board.getSize();

			for(int column = 0; column < board.getSize(); column++){
				index2[0] = column;
				//Check for occupation
				if(board.getFieldValue(index2) != null && columns == null)
					columns = board.getFieldValue(index2);
				//Check for occupation conflict
				else if(board.getFieldValue(index2) != null && columns != board.getFieldValue(index2))
					break;
				//Check for occupation continuation
				else if(board.getFieldValue(index2) != null && columns == board.getFieldValue(index2))
					marks--;
				//Check for end
				if(row == board.getSize() - 1){
					if(this != columns && columns != null){
						param[2]++;
						if(marks < param[4])
							param[4] = marks;
					}
					else if(this == columns){
						param[1]++;
						if(marks < param[3])
							param[3] = marks;
					}
				}
			}
			// ------ end row search
		}
		// ------ begin vertical search
	}

	index2[0]=index2[1]=index2[2]=0;

	if(board.getDimensions() == 3){
		for(int row = 0; row < board.getSize(); row++){
				index2[1] = row;
				//Notation for already seen Player in a column
				IPlayer columns = null;
				int marks = board.getSize();

				for(int column = 0; column < board.getSize(); column++){
					index2[0] = column;
					for(int layer = 0; layer < board.getSize(); layer++){
						index2[2] = layer;
						//Check for occupation
						if(board.getFieldValue(index2) != null && columns == null)
							columns = board.getFieldValue(index2);
						//Check for occupation conflict
						else if(board.getFieldValue(index2) != null && columns != board.getFieldValue(index2))
							break;
						//Check for occupation continuation
						else if(board.getFieldValue(index2) != null && columns == board.getFieldValue(index2))
							marks--;
						//Check for end
						if(layer == board.getSize() - 1){
							if(this != columns && columns != null){
								param[2]++;
								if(marks < param[4])
									param[4] = marks;
							}
							else if(this == columns){
								param[1]++;
								if(marks < param[3])
									param[3] = marks;
							}
						}
					}
				}
				// ------ end row search
			}
		}

		return param;
	}

	/**
	 * Learns the weights based on the winner of the match
	 */
	public void onMatchEnds(IBoard board) {
		// calculate error
		matches++;
		float currentBoardState = 0;
		if(board.getWinner() == null)
			currentBoardState = 50;
		else if(board.getWinner() == this)
			currentBoardState = 100;
		else{
			currentBoardState = -100;
			lost++;
		}
		float error = Math.abs(classifyBoard(board) - currentBoardState);
		LMS(board, error);
		//System.out.println("------------------------Required Moves: " + moves);
		//float stat= (float) lost/ (float)matches;
		//System.out.println(lost + " out of " +matches +" --- "+ stat);
		moves = 0;
		return;
	}

}
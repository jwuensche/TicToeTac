import de.ovgu.dke.teaching.ml.tictactoe.api.IBoard;
import de.ovgu.dke.teaching.ml.tictactoe.api.IPlayer;
import de.ovgu.dke.teaching.ml.tictactoe.api.IllegalMoveException;
import de.ovgu.dke.teaching.ml.tictactoe.game.Move;

/**
 * 
 * @author Marten Wallewein-Eising, Johann Wagner, Johannes Wuensche
 */

public class NewPlayer implements IPlayer {
	//float w0, w1, w2, w3, w4;
	float learningRate = 0.001f;
	float[] weights = {0, 10, -10, -10, 10 };
	
	
	public NewPlayer(){
		//w0 = w1 = w2 = w3 = w4= 1.0f;
	}
	
	public String getName() {
		// TODO Auto-generated method stub
		return "the name of your player";
	}

	public int[] makeMove(IBoard board) {
		// TODO Auto-generated method stub

		// create a clone of the board that can be modified
		IBoard copy = board.clone();

		// do a move using the cloned board
		try {
			copy.makeMove(new Move(this, new int[] { 0, 0, 0 }));
		} catch (IllegalMoveException e) {
			// move was not allowed
		}

		// return your final decision for your next move
		return new int[] { 1, 2, 3 };
	}
	
	private void LMS(IBoard boardPrev, IBoard boardAft){
		int[] params = this.getParameters(boardAft);
		float moveValue = this.classifyMove(boardPrev, boardAft);
		
		for(int i = 0; i < params.length; ++i)
		{
			this.weights[i] = this.weights[i] + this.learningRate * params[i]* moveValue;
		}
		
		/*
		this.w0 = this.w0 + this.learningRate * 1 * moveValue;
		this.w1 = this.w1 + this.learningRate * param[0]* moveValue;
		this.w2 = this.w2 + this.learningRate * param[1]* moveValue;
		this.w3 = this.w3 + this.learningRate * param[2]* moveValue;
		this.w4 = this.w4 + this.learningRate * param[3]* moveValue;
		*/
	}
	
	private float classifyMove(IBoard boardPrev, IBoard boardAft){
		return this.classifyBoard(boardAft) - this.classifyBoard(boardPrev);
	}
	
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
		// stuff
		//return
		return null;
	}

	public void onMatchEnds(IBoard board) {
		return;
	}

}

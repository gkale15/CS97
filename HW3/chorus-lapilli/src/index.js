import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(i) {
    return (
      <Square
        value={this.props.squares[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [{
        squares: Array(9).fill(null)
      }],
      stepNumber: 0,
      xIsNext: true,
      xisSet: false,
      oisSet: false,
      memO:10,
      memX:10,
    };
  }

  handleClick(i) {
    const history = this.state.history.slice(0,this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();

    if (this.state.stepNumber > 5) {
      if (calculateWinner(squares)) {
        return;
      }

      if(squares[i] == 'X' & this.state.xIsNext) {
        this.setState({
          xisSet: true,
          memX: i,
        });
      }

      else if(squares[i] == 'O' && !this.state.xIsNext) {
        this.setState({
          oisSet: true,
          memO: i,
        });
      }

      if (this.state.xisSet && isValidMove(squares,i,this.state.memX,this.state.xIsNext)) {
        squares[i] = 'X';
        squares[this.state.memX] = null;
        this.setState({
          history: history.concat([{
          squares: squares
        }]),
          stepNumber: history.length,
          xIsNext: false,
          xisSet: false,
        });
      }

      else if (this.state.oisSet && isValidMove(squares,i,this.state.memO,this.state.xIsNext)) {
        squares[i] = 'O';
        squares[this.state.memO] = null;
        this.setState({
          history: history.concat([{
          squares: squares
        }]),
          stepNumber: history.length,
          xIsNext: true,
          oisSet: false,
        });
      }

      return;
    }

    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    squares[i] = this.state.xIsNext ? 'X' : 'O';
    this.setState({
      history: history.concat([{
        squares: squares
      }]),
      stepNumber: history.length,
      xIsNext: !this.state.xIsNext,
    });
  }
  
  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step%2) == 0,
    });
  }

  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);

    const moves = history.map((step,move) => {
      const desc = move ?
        'Go to move #' +move :
        'Go to game start';
      return (
        <li key={move}> 
          <button onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });

    let status;
    if (winner) {
      status = 'Winner: ' + winner;
    } else {
      status = 'Next player: ' + (this.state.xIsNext ? 'X' : 'O');
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={(i) => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function isAdjacent(squares,i,memPawn) {
  if(memPawn ==  0) {
    if((i == 1 || i == 3 || i == 4) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  1) {
    if((i == 0 || i == 2 || i == 4 || i == 5 || i == 3) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  2) {
    if((i == 1 || i == 5 || i == 4) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  3) {
    if((i == 1 || i == 0 || i == 4 || i == 6 || i == 7) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  4) {
    if(squares[i] == null) {
      return true;
    } 
  }
  if(memPawn ==  5) {
    if((i == 1 || i == 2 || i == 4 || i == 8 || i == 7) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  6) {
    if((i == 3 || i == 7 || i == 4) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  7) {
    if((i == 3 || i == 5 || i == 4 || i == 6 || i == 8) && squares[i] == null){
      return true;
    } 
  }
  if(memPawn ==  8) {
    if((i == 7 || i == 5 || i == 4) && squares[i] == null){
      return true;
    } 
  }
  return null;
}



function isValidMove(squares,i,memPawn,xFlg) {
  const squares_temp = squares.slice();
  if(xFlg) {
    squares_temp[i] = 'X';
    squares_temp[memPawn] = null;
  }
  else if (!xFlg) {
    squares_temp[i] = 'O';
    squares_temp[memPawn] = null;
  }


  if(((xFlg && squares[4] == 'X') || (!xFlg && squares[4] == 'O')) && memPawn != 4){
    if(isAdjacent(squares,i,memPawn) && calculateWinner(squares_temp)) {
      return true;
    }
    else {
      return null;
    }
  }

  else{
    return (isAdjacent(squares,i,memPawn))
  }

  return null;
}

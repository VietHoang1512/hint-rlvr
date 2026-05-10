from .evaluator import *
from .evaluators.graph_problems_eval import *
from .evaluators.twentyfourpoints_evaluator import *
from .evaluators.calcudoku_eval import *
from .evaluators.cryptomath_eval import *
from .evaluators.kukurasu_eval import *
from .evaluators.skyscrapers_evaluator import *
from .evaluators.wordladder_eval import *

from .evaluators.aquarium_eval import *
from .evaluators.binario_eval import *
from .evaluators.campsite_eval import *
from .evaluators.eulero_eval import *
from .evaluators.futoshiki_eval import *
from .evaluators.hanoi_eval import *
from .evaluators.hitori_eval import *
from .evaluators.nonogram_eval import *
from .evaluators.bridges_eval import *
from .evaluators.kakuro_eval import *
from .evaluators.maze_eval import *
from .evaluators.minesweeper_eval import *
from .evaluators.nibbles_eval import *
from .evaluators.numbrix_eval import *
from .evaluators.slidingpuzzle_eval import *
from .evaluators.sokoban_eval import *
from .evaluators.snake_eval import *
from .evaluators.wordsearch_eval import *
from .evaluators.shingoki_eval import *
from .evaluators.tapa_eval import *
from .evaluators.sudoku_evaluator import *

metrics = {
    'simple_str_match': SimpleStrMatch(),
    'match_from_list': MatchFromList(),
    'sliding_puzzle_evaluator': SlidingPuzzleEvaluator(),
    'eulero_evaluator': EuleroEvaluator(),
    'hanoi_evaluator': TowerOfHanoiEvaluator(),
    'maze_evaluator': MazeEvaluator(),
    'minesweeper_evaluator': MinesweeperEvaluator(),
    'numbrix_evaluator': NumbrixEvaluator(),
    'sokoban_evaluator': SokobanEvaluator(),
    'snake_evaluator': SnakeEvaluator(),
    'wordsearch_evaluator': WordSearchEvaluator(),
    'hamiltonian_path_evaluator': HamiltonianPathEvaluator(),
    'hamiltonian_cycle_evaluator': HamiltonianCycleEvaluator(),
    'eulerian_path_evaluator': EulerianPathEvaluator(),
    'eulerian_cycle_evaluator': EulerianCycleEvaluator(),
    'topological_sort_evaluator': TopologicalSortEvaluator(),
    '24points_evaluator': TwentyFourPointsEvaluator(),
    'calcudoku_evaluator': CalcudokuEvaluator(),
    'cryptomath_evaluator': CryptoMathEvaluator(),
    'kukurasu_evaluator': KukurasuEvaluator(),
    'skyscrapers_evaluator': SkyscrapersEvaluator(),
    'wordladder_evaluator': WordLadderEvaluator(),
    'aquarium_evaluator': AquariumEvaluator(),
    'binairo_evaluator': BinarioEvaluator(),
    'campsite_evaluator': CampsiteEvaluator(),
    'futoshiki_evaluator': FutoshikiEvaluator(),
    'hitori_evaluator': HitoriEvaluator(),
    'nonogram_evaluator': NonogramsEvaluator(),
    'bridges_evaluator': BridgesEvaluator(),
    'kakuro_evaluator': KakuroEvaluator(),
    'shingoki_evaluator': ShingokiEvaluator(),
    'tapa_evaluator': TapaEvaluator(),
    'nibbles_evaluator': NibblesEvaluator(),
    'connectivity_evaluator': ConnectivityEvaluator(),
    'sudoku_evaluator': SudokuEvaluator(),
    'unsupported': SimpleStrMatch(),
}

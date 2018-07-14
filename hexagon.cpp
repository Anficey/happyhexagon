#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

struct piece
{
	int d[3];
};

const piece A0 = {-1, -1, -1};
const piece P[23] = {
	#include "pieceData.inc"
};

struct step
{
	int piece_index;
	int pos;
};


struct hexagon
{
	int status;
	struct hexagon *d[6];
};

class board
{
public:
	hexagon cell[61];
	
	board()
	{
		int d[6][61] = {
			#include "directionData.inc"
		};
		for (int i = 0; i < 61; ++i)
		{	
			cell[i].status = 0;
			for (int j = 0; j < 6; ++j)
				cell[i].d[j] = (d[j][i] != -1) ? (&cell[d[j][i]]) : NULL;
		}
	}

	board(string filename)
	{
		ifstream board_file(filename);
		int d[6][61] = {
			#include "directionData.inc"
		};
		for (int i = 0; i < 61; ++i)
		{	
			cell[i].status = board_file.get() - '0';
			for (int j = 0; j < 6; ++j)
				cell[i].d[j] = (d[j][i] != -1) ? (&cell[d[j][i]]) : NULL;
		}
	}

	board(const board &t)
	{
		int d[6][61] = {
			#include "directionData.inc"
		};
		for (int i = 0; i < 61; ++i)
		{	
			cell[i].status = t.cell[i].status;
			for (int j = 0; j < 6; ++j)
				cell[i].d[j] = (d[j][i] != -1) ? (&cell[d[j][i]]) : NULL;
		}
	}
	
	int clear_hexagon(int piece_index, int pos)
	{
		
		int before0 = place_piece(piece_index,pos).check_line().count(0);
		int after0 = count(0);
		if(piece_index != -1)
			return before0 - after0;
		else
			return before0 - after0;
	}

	board place_piece(int piece_index, int pos)
	{
		board b = board(*this);
		b.cell[pos].status = 1;

		if(piece_index != -1)
		{
			auto ptr = &b.cell[pos];
			for(int i = 0; i < 4 &&  ptr != NULL ; ptr = ptr -> d[P[piece_index].d[i++]])
			{
				ptr -> status = 1;
			}
		}
		return b;
	}
	
	board show_step(step s)
	{
		board b = board(*this);
		b.cell[s.pos].status = 2;
		if(s.piece_index != -1)
		{
			auto ptr = &b.cell[s.pos];
			for(int i = 0; i < 4 &&  ptr != NULL ; ptr = ptr -> d[P[s.piece_index].d[i++]])
			{
				ptr -> status = 2;
			}
		}
		return b;
	}

	board place_piece(step s)
	{
		return place_piece(s.piece_index, s.pos);
	}

	int count(int n)
	{
		int ans = 0;
		for (int i = 0; i < 61; ++i)
			if(cell[i].status == n)
				ans += 1;
		return ans;
	}
	
	board check_line()
	{
		board b = board(*this);
		int head[3][9] = {
			#include "headData.inc"
		};
		for (int i = 0; i < 3; ++i)
		{
			for (int j = 0; j < 9; ++j)
			{
				auto ptr = &b.cell[head[i][j]];
				for(; ptr != NULL; ptr = ptr -> d[i])
					if(ptr -> status == 0)
						break;
				if(ptr == NULL)
				{
					auto ptr = &b.cell[head[i][j]];
					for(; ptr != NULL; ptr = ptr -> d[i])
						ptr -> status = 3;
				}
			}
		}
		for (int i = 0; i < 61; ++i)
			if (b.cell[i].status == 3)
				b.cell[i].status = 0;
		return b;
	}

	vector<int> solution(int piece_index)
	{
		vector<int> ans;
		ans.reserve(61);
		if (piece_index == -1)
		{
			for (int i = 0; i < 61; ++i)
			{
				if(cell[i].status == 0)
					ans.push_back(i);
			}
			return ans;
		}
		for (int i = 0; i < 61; ++i)
		{
			if(cell[i].status == 0)
			{
				int j = 0;
				for(auto ptr = &cell[i]; ptr != NULL && j <= 3; ptr = ptr -> d[P[piece_index].d[j++]])
				{
					if(ptr -> status != 0)
						break;
				}
				if(j == 4)
					ans.push_back(i);
			}
		}
		return ans;
	}
	
	int solution_count(int piece_index)
	{
		int ans;
		if (piece_index == -1)
		{
			ans = count(0);
			return ans;
		}
		for (int i = 0; i < 61; ++i)
		{
			if(cell[i].status == 0)
			{
				int j = 0;
				for(auto ptr = &cell[i]; ptr != NULL && j <= 3; ptr = ptr -> d[P[piece_index].d[j++]])
				{
					if(ptr -> status != 0)
						break;
				}
				if(j == 4)
					ans++;
			}
		}
		return ans;
	}

	double solution_score_deep(vector<int> piece_index)
	{
		double max_score = 0;

		for(int choice_i = 0; choice_i < piece_index.size(); choice_i++)
		{
			for(auto& pos_i : solution(piece_index[choice_i]))
			{
				double score = 0;

				score += clear_hexagon(piece_index[choice_i], pos_i) * 0.4;
				
				for(int choice_j = 0; choice_j < piece_index.size(); choice_j++)
				{
					board b = place_piece(piece_index[choice_i], pos_i).check_line();
					score += b.solution_count(piece_index[choice_j]) * 0.5;
				}
				if(score >= max_score)
				{
					max_score = score;
				}
			}
		}
		return max_score;
	}

	step best_solution(vector<int> piece_index)
	{
		int choice, pos;
		double max_score = 0;
		
		for(int choice_i = 0; choice_i < piece_index.size(); choice_i++)
		{
			for(auto& pos_i : solution(piece_index[choice_i]))
			{

				double score = 0;

				score += clear_hexagon(piece_index[choice_i], pos_i);
				for(int choice_j = 0; choice_j < piece_index.size(); choice_j++)
				{
					vector<int> piece_index_deep1;
					piece_index_deep1.reserve(2);

					board b = place_piece(piece_index[choice_i], pos_i).check_line();

					if(choice_j != choice_i)
					{
						int solution_count = b.solution_count(piece_index[choice_j]);
						piece_index_deep1.push_back(piece_index[choice_j]);
						score += solution_count * 0.7;
						if(solution_count == 0)
							score -= 10000;
						score += b.solution_score_deep(piece_index_deep1) * 0.5;
					}
				}
				if(score >= max_score)
				{
					max_score = score;
					choice = choice_i;
					pos = pos_i;
				}
			}
		}
		step ans;
		ans.piece_index = piece_index[choice];
		ans.pos = pos;
		return ans;
	}
};

inline
std::ostream& operator << (std::ostream& strm, const board& f)
{
	int row_end = 4, row = 0;
	strm << "    ";
	for (int i = 0; i < 61; ++i)
	{
		switch(f.cell[i].status)
		{
			case 0: strm << "-";break;
			case 1: strm << "x";break;
			case 2: strm << "o";break;
			case 3: strm << "~";break;
			default: strm << "?";
		}
		strm  << " ";
		if(i == row_end)
		{
			row++;
			row_end += (9 - abs(4 - row));
			strm << endl;
			for (int j = 0; j < abs(4 - row) && row != 9; ++j)
				strm << " ";
		}
	} 
	return strm;
}

void load_piece(vector<int> &p)
{
	ifstream piece_file("_piece.txt");
	for (int i = 0; i < 3; ++i)
	{/**/
		int j = piece_file.get() - 'a' - 1;
		p[i] = j;
	}
}

int main(int argc, char const *argv[])
{
	ofstream ans_file("_answer.txt");
	board b = board("_board.txt");
	vector<int> p(3);
	load_piece(p);
	if(argc == 1)
	{
		cout << "[";
		for(int i = 0; i < 3; i++)
		{
			char c = 'a' + p[i] + 1;
			cout << c << ",";
		}
		cout << "]" << endl;
		cout << b << endl;
	}
	
	
	step s = b.best_solution(p);

	if(argc == 1)
	{
		cout << endl << s.piece_index << "," << s.pos << endl; 
	}
	
	cout << b.show_step(s);

	ans_file << "(" << s.piece_index << "," << s.pos << ")";
	return 0;
}


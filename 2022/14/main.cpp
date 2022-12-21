#include <iostream>
#include <fstream>
#include <sstream>

int map[1000][1000] = {0};
const int WALL = 1;
const int SPACE = 0;
const int SAND = 2;

void drawLine(int x1, int y1, int x2, int y2)
{
        if (x1 == x2)
        {
                int ymin = std::min(y1, y2);
                int ymax = std::max(y1, y2);
                for (int y = ymin; y <= ymax; y++)
                {                       
                        map[x1][y] = WALL;
                }
        }
        if (y1 == y2)
        {
                int xmin = std::min(x1, x2);
                int xmax = std::max(x1, x2);
                for (int x = xmin; x <= xmax; x++)
                {                       
                        map[x][y1] = WALL;
                }
        }
}

void printMap()
{
        for (int y = 0; y < 1000; y++)
        {
                for (int x = 0; x < 1000; x++)
                {
                        char vis[] = " #o";
                        std::cout << vis[map[x][y]];
                }
                std::cout << std::endl;
        }
}

void parseMap(const char* filename)
{
        std::ifstream in(filename);
        if (not in.is_open())
        {
                std::cerr << "Bad file" << std::endl;
                return ;
        }
        std::string line;
        while (std::getline(in, line))
        {
                std::istringstream ss(line);
                int lastX = 0;
                int lastY = 0;
                while (ss)
                {
                        int x, y;
                        char c;
                        std::string s;
                        
                        ss >> x >> c >> y;
                        ss >> s;
                        
                        if (lastX != 0)
                        {
                                drawLine(x, y, lastX, lastY);
                                
                        }
                        
                        lastX = x;
                        lastY = y;
                }
        }
}

bool pourSand()
{
        int x = 500;
        int y = 0;
        
        while (true)
        {
                if (map[x][y+1] == SPACE)
                {
                        y++;
                } else if (map[x-1][y+1] == SPACE)
                {
                        x--;
                        y++;
                } else if (map[x+1][y+1] == SPACE)
                {
                        x++;
                        y++;
                } else
                {
                        map[x][y] = SAND;
                        break;
                }
                if (y == 1000)
                {
                        return false;
                }
        }
        return true;
}

void drawBottom()
{
        int lowestY = 0;
        for (int y = 999; y > 0; y--)
        {
                for (int x = 0; x < 1000; x++)
                {
                        if (map[x][y] != SPACE)
                        {
                                lowestY = y;
                                break;
                        }
                }
                if (lowestY != 0)
                {
                        break;
                }
        }
        
        int bottomY = lowestY + 2;
        for (int x = 0; x < 1000; x++)
        {
                map[x][bottomY] = WALL;
        }              
}

void clearMap()
{
        for (int y = 0; y < 1000; y++)
        {
                for (int x = 0; x < 1000; x++)
                {
                        map[x][y] = SPACE;
                }
        }
}

int main(int argc, char *argv[])
{
        parseMap(argv[1]);
        int i = 0;
        while (pourSand())
        {
                i++;
        }
        std::cerr << i << std::endl;
        printMap();

        clearMap();

        parseMap(argv[1]);
        drawBottom();
        
        i = 0;
        while (map[500][0] == SPACE)
        {
                pourSand();
                i++;
        }
        printMap();
        std::cerr << i << std::endl;
        return 0;
}
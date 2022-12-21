#include <iostream>

#include <algorithm>
#include <vector>

std::vector<int> parseFile()
{
        auto file = fopen("input.txt", "r");
        char buffer[10];
        std::vector<int> values;
        int sum = 0;
        
        while (not feof(file))
        {
                buffer[0] = 0;
                fgets(buffer, sizeof(buffer), file);
                if (buffer[0] == '\n')
                {
                        values.push_back(sum);
                        printf("%d\n", sum);
                        sum = 0;
                }
                else
                {
                        int i = atoi(buffer);
                        sum += i;
                }
        }        
        return values;
}

int main()
{
        std::vector<int> values = parseFile();
        auto max = std::max_element(values.begin(), values.end());
        printf("%d\n", *max);
        
        std::sort(values.begin(), values.end());
        int sum = 0;
        for (int i = values.size() - 3; i < values.size(); i++)
        {
                sum += values[i];
        }
        printf("%d\n", sum);
        return 0;
}
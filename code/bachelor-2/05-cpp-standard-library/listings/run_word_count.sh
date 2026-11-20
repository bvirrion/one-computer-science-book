# capture: session copy=words.hpp,word_count.cpp,books.csv
g++ -std=c++20 -O2 -Wall -Wextra word_count.cpp -o word_count
head -3 books.csv
./word_count < books.csv

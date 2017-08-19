#include <iostream>
#include <unordered_map>
#include <set>
#include <string>

using namespace std;

void eraseFromMap(unordered_map<char, int> &tmap, char data)
{
    if (tmap.find(data) == tmap.end())
        return;
   
    if (tmap[data] > 1)
    {
        tmap[data] -= 1;
    }
    else
    {
        tmap.erase(data);
    }
}

void insertToMap(unordered_map<char, int> &tmap, char data)
{
    if (tmap.find(data) != tmap.end())
    {
        tmap[data] += 1;
    }
    else
    {
        tmap[data] = 1;
    }
}

bool compareMaps(unordered_map<char, int> &nmap, unordered_map<char, int> &hmap)
{
    if (nmap.size() != hmap.size())
        return false;

    for ( auto h : hmap)
    {
        if (nmap.find(h.first) != nmap.end())
        {
            if (nmap[h.first] != h.second)
                return false;
        }
        else
            return false;
    }
    return true; 
}

int main()
{
    string needle = "AAB";
    string haystack = "ABADEDBAAABD";

    unordered_map<char, int> hmap;
    unordered_map<char, int> nmap;
    set<int> idxSet;

    for (int i=0; i < needle.size() ; i++)
       insertToMap(nmap, needle.at(i));

    for (int i= 0; i < haystack.size(); ++i)
    {
        insertToMap(hmap, haystack.at(i));
        if (i >= (needle.size() - 1))
        {
            if (compareMaps(nmap, hmap))
                idxSet.insert(i - needle.size() + 1);
            eraseFromMap(hmap, haystack.at(i - needle.size() + 1));
        }
    }
    if (idxSet.size() > 0)
    {
        set<int>::const_iterator cit = idxSet.begin();
        cout << *cit;
        cit++;
        while (cit != idxSet.end())
        {
            cout << ", " << *cit;
            cit++;
        }
        cout <<endl;
    }
    return 0;           
}

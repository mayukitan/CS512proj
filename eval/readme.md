# Test Result Format

The format of test result csv file is as follows:

```
TestSubjectA,1stSimilarToA,2ndSimilarToA,3rdSimilarToA,...,lastSimilarToA
TestSubjectB,1stSimilarToB,2ndSimilarToB,3rdSimilarToB,...,lastSimilarToB
TestSubjectC,1stSimilarToC,2ndSimilarToC,3rdSimilarToC,...,lastSimilarToC
...
```


For example, let's say we have three test subjects:

  * `chiahao`, who has these top 4 similar actors: `chiahao` himself, `chia100`, `hao42`, and `hsieh20` (in descending order)
  * `letang`, who has top 4 similar actors: `letang` himself, `le2016`, `tang33`, and `boon22` (in descending order)
  * `hanqing`, who has top 4 similar actors: `hanqing` himself, `han68`, `qing5`, and `chen89` (in descending order)

Then the test result should look like:

```
chiahao,chiahao,chia100,hao42,hsieh20
letang,letang,le2016,tang33,boon22
hanqing,hanqing,han68,qing5,chen89
```

You could also open `example.csv` to see an example test result csv file.

Note that there is no constraint on the order of test subjects.
You can switch lines if you want.

For instance, the following test result works effectively the same as the one above:
```
hanqing,hanqing,han68,qing5,chen89
letang,letang,le2016,tang33,boon22
chiahao,chiahao,chia100,hao42,hsieh20
```

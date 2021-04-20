Describe your algorithm here
======
first we compute the ratio of diffrence between a bit rate and the next to the first bit rate. we save this ratios.

at initial we return quality 0, chunk 0 and timeout 0
in case of rebuffer or timeout we redownload, i should have made the quality 0, i forgot

when a chunk finishes downloading, we compute how many chunks we have in the buffer and how long it took to download the current chunk.
we define m, which is the ratio of 4.0 seconds to how long it took to download the current chunk

if the buffer has more than the minimal amount allowed and if the qaulity is not allready the max, and if a condition is meet on m using the precomputed rarios between bit rates or if the buffer has more than a certain amount of chunks, we increase the quality by 1.

if the buffer has less than the minimal amount, we decrease the quality, computed using m.

that's it.

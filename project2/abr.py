from enum import Enum


class CALLBACK_EVENT( Enum ):
    INIT = 0
    DOWNLOAD_COMPLETED = 1
    TIMEOUT  = 2
    REBUFFERING = 3
bit_rate_a = [300,750,1200,1850,2850,4300]
bit_rate_d = [4300,2850,1850,1200,750,300]
chunk_download_start = []
b_m = 4
b_c = 0
MSD = 4.0


def determine_e(bit_rates):
    e = []
    for i in range(len(bit_rates) -1):
        e.append((bit_rates[i+1]- bit_rates[i])/bit_rates[i])
    return e

e = determine_e(bit_rate_a)
print(e)

def abr(
    typ,
    current_time,
    playback_time,
    playback_chunk,
    current_chunk,
    current_chunk_quality,
    current_chunk_download,
    video
):
    """
        typ - type of event
            INIT - initial call at time 0
            DOWNLOAD_COMPLETED - a chunk has been downloaded
            TIMEOUT - timeout has happend
            REBUFFERING - rebuffering started
        
        current_time - time from the beginning of the simulation in seconds
        
        playback_time - how much of the video has been shown (in seconds)
        playback_chunk - the chunk that is playing right now
        current_chunk - the chunk number that is downloading right now (or has been just finished)
        current_chunk_quality - the quality of the current_chunk
        current_chunk_download - how much of current_chunk has been downloaded (in bytes)
        video - contains 6 video arrays (one per quality level) - Each subarray contain the size of each chunk in the video

        Returns
            quality_to_download_now, chunk_to_download_now, timeout

        ABR function returns the next chunk that should be downloaded
           * quality_to_download_now - quality of the next chunk from 0 to 5
           * chunk_to_download_now   - chunk number of the chunk that should be downloaded
                                     - next_chunk cannot be in the past, if the player plays chunk 10, chunk 9 shouldn't be downloaded
                                     - if you set next_chunk to -1, no chunk will be downloaded
                                     - if the previou download hasn't been completed (e.g. in case of rebuffering) you can change the chunk
                                       that is currently downloading. For instance, you started downloading a high quality chunk, but
                                       rebuffering happened and now you would like to lower the quality. In that case, return the same chunk
                                       number, but different quality.
           * timeout    - set a timer that will trigger the abr function again
                        - timeout is in absolute time, usually set it as current_time+X (where min X is 200ms)
                        - timeout 0 means no timeout
    """
    
    #initial
    if typ == CALLBACK_EVENT.INIT:
        chunk_download_start.append(current_time)
        return 0, 0, 0.0

    #rebuffering or timeout, ignore 
    if typ == CALLBACK_EVENT.TIMEOUT or typ == CALLBACK_EVENT.REBUFFERING:
        return current_chunk_quality, current_chunk, 0


    next_chunk = current_chunk + 1
    
    #if we arrived to the end of the stream or it is not the initial call and the download has finished
    
    
    if next_chunk == len(video[0]):
        next_chunk = -1

    

    if typ == CALLBACK_EVENT.DOWNLOAD_COMPLETED:
        next_quality = current_chunk_quality
        b_c = current_chunk - playback_chunk
        SFT = current_time - chunk_download_start[current_chunk] 
        #print("sft", SFT)
        m = MSD/SFT
        #print("m", m)
        if( b_c > b_m and current_chunk_quality < 5 and m > 1 + e[current_chunk_quality] ) or (current_chunk_quality < 5  and b_c > 10):
                print("switch up")
                next_quality = current_chunk_quality +1

        
        
        if b_c < b_m:
            print("switch down")
            for b in bit_rate_d:
                next_quality = 0
                if b < m * current_chunk_quality:
                    next_quality = bit_rate_a.index(b)
                    continue
        
        chunk_download_start.append(current_time)
        print("b_c", b_c ,"sft", SFT, "m", m, "next quality " , next_quality, "next chunk " , next_chunk)
        return next_quality, next_chunk, 0

       
        

    
    return 0, next_chunk, 0

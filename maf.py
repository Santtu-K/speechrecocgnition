# Moving average filter
def MA_filter(sound, wnd):
    n_sample = len(sound)
    res = [0]*n_sample
    temp = 0
    # First value
    for q in range(wnd):
        temp = temp + abs(sound[q])
    res[0] = temp / wnd
    for i in range(1,n_sample-wnd):
        res[i] = res[i-1] + (abs(sound[i+wnd])-abs(sound[i-1]))/wnd    
    # viimeiset wnd arvoa
    q = 0
    for j in range(n_sample-wnd, n_sample):
        res[j] = (res[j-1]*(wnd-q)-abs(sound[j-1]))/(wnd+q+1)
        q = q + 1
    return res
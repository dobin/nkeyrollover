import pstats
p = pstats.Stats('perf.txt')
p.sort_stats('cumulative').print_stats()

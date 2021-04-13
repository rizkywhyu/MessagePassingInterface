import time
from mpi4py import MPI

def loop(num_steps,awal,akhir):
    step = 1.0/num_steps
    sum = 0
    for i in xrange(awal,akhir):
        x= (i+0.5) * step
        sum = sum +4.0/(1.0+x*x)
    return sum

def Pi(num_steps):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    start = time.time()
    
    pembagi = num_steps/size

    awal = rank * pembagi
    
    akhir = awal + pembagi-1
    print "step %d - %d ke rank %d \n" % (awal,akhir,rank)
    local_sum = loop(num_steps, awal, akhir)
    sum = comm.reduce(local_sum, op=MPI.SUM, root=0)
    akhir = time.time()
    if rank == 0:
        print "step awal adalah",num_steps
        print "step dibagi menjadi %d bagian" % (pembagi)

        pi = sum / num_steps
        print "Pi with %d steps is %.20f in %f secs" % (num_steps, pi, akhir - start)


if __name__ == '__main__':
    Pi(100)

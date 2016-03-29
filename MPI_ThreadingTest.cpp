/* Requests the highest level of MPI thread safety (MPI_THREAD_MULTIPLE) and the one provided by the MPI implementation. */

#include <mpi.h>
#include <iostream>

using std::cout;
using std::endl;

int main(int argc, char *argv[])
{
  int provided = 0;
  MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE , &provided);
  cout << "provided = " << provided << endl;
  switch (provided) {
  case MPI_THREAD_SINGLE:
    cout << "MPI_THREAD_SINGLE provided." << endl;
    break;
  case MPI_THREAD_FUNNELED:
    cout << "MPI_THREAD_FUNNELED provided." << endl;
    break;
  case MPI_THREAD_SERIALIZED:
    cout << "MPI_THREAD_SERIALIZED provided." << endl;
    break;
  case MPI_THREAD_MULTIPLE:
    cout << "MPI_THREAD_MULTIPLE provided." << endl;
    break;
  }
  
  MPI_Finalize();

  cout << "Information see https://www.open-mpi.org/doc/v1.8/man3/MPI_Init_thread.3.php" << endl;
}


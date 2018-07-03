/* Requests the highest level of MPI thread safety (MPI_THREAD_MULTIPLE) and the one provided by the MPI implementation. */

#include <mpi.h>
#include <iostream>

using std::cout;
using std::endl;

int main(int argc, char *argv[])
{
  if (argc == 1) {
    cout << "Usage: " << argv[0] << " {init | query}" << endl;
    return 0;
  }
  std::string arg = argv[1];
  int provided = -1;
  
  if (arg == "init") {
    cout << "Trying to initialize for MPI_THREAD_MULTIPLE" << endl;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE , &provided);
    cout << "provided = " << provided << endl;
  }
  if (arg == "query") {
    MPI_Init(&argc, &argv);
    cout << "Querying default thread level" << endl;
    MPI_Query_thread(&provided);
  }
  switch (provided) {
  case MPI_THREAD_SINGLE:
    cout << "MPI_THREAD_SINGLE detected." << endl;
    break;
  case MPI_THREAD_FUNNELED:
    cout << "MPI_THREAD_FUNNELED detected." << endl;
    break;
  case MPI_THREAD_SERIALIZED:
    cout << "MPI_THREAD_SERIALIZED detected." << endl;
    break;
  case MPI_THREAD_MULTIPLE:
    cout << "MPI_THREAD_MULTIPLE detected." << endl;
    break;
  }
  
  MPI_Finalize();

  cout << "Information see https://www.open-mpi.org/doc/v1.8/man3/MPI_Init_thread.3.php" << endl;
}


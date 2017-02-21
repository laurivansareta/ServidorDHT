import sys

from distribuicaoArquivos import DistribuicaoArquivos

servidor = DistribuicaoArquivos(sys.argv[1], sys.argv[2:])
servidor.run()

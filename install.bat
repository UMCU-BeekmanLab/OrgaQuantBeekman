call mkdir env
call tar -xzf env.tar.gz -C env
call env\Scripts\activate
call conda-unpack
call jupyter contrib nbextension install --sys-prefix
call jupyter nbextension enable hide_input_all
PAUSE
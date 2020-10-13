# automacao_workshops
Repositório com códigos em Python úteis para geração e envio de certificados, de forma automática  

## Preenchimento automático de certificados
1. Instale as bibliotecas necessárias, através do terminal, caso ainda não as tenha
```bash
pip install pillow
pip install pandas 
```
2. Faça um clone deste repositório, ou baixe em um arquivo .ZIP e descompacte
3. Adicione o modelo do certificado (com o nome *modelo.png*) à pasta *recursos*
4. Adicione um arquivo CSV com os nomes das pessoas (com o nome *nomes.csv*, a coluna deve ser intitulada como *Nomes*) à pasta *recursos*
5. Baixe um modelo de fonte que queira utilizar ([neste site, por exemplo](https://www.dafont.com/))
6. Adicione o arquivo .ttf da fonte à pasta *recursos*, com o nome *fonte.ttf*
7. Delete os exemplos da pasta *certificados*. É onde os certificados serão salvos
8. Caso queira alterar o tamanho da fonte, a posição do nome ou qualquer outra informação, altere o arquivo **preencher_certificados.py**
9.  Por fim, rode o arquivo **preencher_certificados.py**, e todos os certificados serão salvos na pasta *certificados*

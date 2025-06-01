program BinarioParaInteiro;

function BinToInt(bin: String): Integer;
var
  i, valor, potencia: Integer;
begin
  valor := 0;
  potencia := 1;

  for i := length(bin) downto 1 do
  begin
    if bin[i] = '1' then
      valor := valor + potencia;
    potencia := potencia * 2;
  end;

  BinToInt := valor;
end;

var
  bin: String;
  valor: Integer;
begin
  writeln('Introduza uma string binária:');
  readln(bin);

  valor := BinToInt(bin);
  writeln('O valor inteiro correspondente é: ', valor);
end.

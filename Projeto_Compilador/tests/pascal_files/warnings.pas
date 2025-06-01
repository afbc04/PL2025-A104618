program SemanticErrors;

function func() : integer;
var
    n : integer; {'n' não é usado}
begin
    func := 1;
end;

procedure proc(); {Procedure não é usado}
begin
    writeln('Hello world');
end;

var
    a : array[1..2] of real; {'a' apenas vai ser lida, não definida}
    b, c : real; {'b' não vai ser lida, e 'c' não é usado}

begin

    b := a[0]; {aceder fora do array}
    b := func() * 1.2;
    b := 1 / 0; {Divisão por zero}

end.
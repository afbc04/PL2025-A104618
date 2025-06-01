program SyntaxErrors;

function func(arg1 : real, arg2 : integer); string; {Declaração de argumentos e formato de função mal definidos}
begin

    arg1 := length(arg2; {Function call mal formada}

end:


var
    a : integer;
    b : string;

begin

    a = 5; {Atribuição tem que ser com :=}
    b := 'Ola mundo' {Falta de ;}

    writeln('PL'[0]); {String literal não pode ser tratada como array}
end.
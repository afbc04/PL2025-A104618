program LexicalErrors;

var
    < : integer; {Nome da variavel não pode ser caracteres especiais}
    @ : string;
    _var : real; {Noma da variavel não pode começar por _}
    a := boolean; {Declarações tem que ter :, e não :=}

begin
    writeln("Everything works just fine"); {String têm que ter blicas, não aspas}
end.
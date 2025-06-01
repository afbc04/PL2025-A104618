program SemanticErrors;

var
    a : integer;
    b : string;
    SemanticErrors : boolean; {Program já tem este nome}

begin

    a := 'Hello world'; {variavel a apenas aceita integers}
    b := func(); {Função tem que existir}

    writeln(c); {C tem que existir}
end.
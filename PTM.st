FUNCTION_BLOCK PTM
  VAR_INPUT
    IN : BOOL;
  END_VAR
  VAR_OUTPUT
    ET : TIME;
  END_VAR
  VAR
    TM : TIME;
    TON1 : TON;
    M : BOOL := FALSE;
  END_VAR

  TON1(
       IN := IN,
       PT := T#10S);
       
  IF IN = TRUE THEN
    TM := TON1.ET;
  ELSIF M = TRUE THEN
    ET := TM;
  ELSE
    M := TRUE;
  END_IF;
END_FUNCTION_BLOCK

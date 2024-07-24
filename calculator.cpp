#include <iostream>
#include <vector>
using namespace std;

// class Token_stream; // member functionss : putback(), get() 
// class Token;        // Token class, member varaibles : kind, value;
double expression();   // Exp = Exp or Exp + Term or Exp - term
double term();         // Term = Term or Term * Primary or Term / Primary
double primary();      // Primary = '(' or Number ; Number = double precision number;
//void error(string);  // Throw errors


//error
void error(string st)
{
    throw runtime_error(st);
}

class Token
{
public:
    char kind;
    double value;
    // Constructor for operators  
    Token(char ch)
        :kind(ch) {} //empty function.

    //constructor for operands
    Token(char ch, double val)
        :kind(ch), value(val) {}
};

class Token_stream
{
private:
    bool full;      // flag for buffer status, empty or full
    Token buffer;   // buffer stores only one token
public:
    Token_stream() :full(false), buffer(0) {};
    Token get();
    void putback(Token t);

};

// save the character which we read and is not used by the respeceted function.
void Token_stream::putback(Token t)
{
    if (full) error("putback() into a full buffer.");
    buffer = t;         //copy t to buffer
    full = true;        //buffer is now full
}

// input character and create Tokens out of it.
Token Token_stream::get()
{
    if (full) {   // check if we have a token already.
        //remove token from buffer
        full = false;
        return buffer;
    }
    // if buffer is empty
    char ch;
    cin >> ch;       // reading new token
    switch (ch)
    {
    case ';':
    case 'q':
    case '(':
    case ')':
    case '+':
    case '-':
    case '*':
    case '/':
    case '%':
        return Token(ch);
        break;
    case '.':
    case '0':
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
        cin.putback(ch); // because we have read a digit (as a character for comparision purpose) which is part of the upcoming stream of digits, so we put it back so we can read it again.
        double val;
        cin >> val;
        return Token('8', val);

    default:
        error("Bad Token");
        break;
    }
}

// Token_stream object
Token_stream ts;

// Primary
double primary()
{
    Token t = ts.get();
    switch (t.kind) {
    case '(':
    {
        double d = expression();
        t = ts.get();
        if (t.kind != ')') error("')' expected");
        return d;
    }
    case '8':
        return t.value;
        break;
    default:
        error("primary expected");
    }

}

// Term
double term()
{
    double left = primary();
    Token t = ts.get();
    while (true) {
        switch (t.kind) {
        case '*':
            left *= primary();
            t = ts.get();
            break;
        case '/':
        {
            double d = primary();
            if (d == 0) error("divided by zero");
            left /= d;
            t = ts.get();
            break;
        }
        default:
            ts.putback(t);
            return left;
        }
    }

}

// Expression
double expression()
{
    double left = term();
    Token t = ts.get();
    while (true) {
        switch (t.kind) {
        case '+':
            left += term();
            t = ts.get();
            break;
        case '-':
            left -= term();
            t = ts.get();
            break;
        default:
            ts.putback(t);
            return left;
        }
    }
}

// execution starts from here
int main()
{
    double val = 0;
    while (cin) {
        Token t = ts.get();
        if (t.kind == 'q') break;                       // Press q to quit
        if (t.kind == ';') cout << "=" << val << endl;   // Press ; to end expression
        else ts.putback(t);
        val = expression();
    }
}
<?php

class X {
    public function __construct(){}
    
    public function display(){
        print_r('!!!');
    }
}

class Y {
    public function display_x(){
        $x = new X();
        $x->display();
    }
}

class Z {
    public $x;
    public function __construct(){
        $this->x = new X();
    }
    public function display_x(){
        $this->x->display();
    }
}

$y = new Y();
$y->display_x();

print_r("\n");

$z = new Z();
$z->display_x();

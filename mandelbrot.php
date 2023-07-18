<?php
function calc_mand($resolution, $precision){
    $x = -0.65; #place on grid
    $y = 0;     #place on grid
    $scale = 3.4;

    $minX = $x - $scale / 2;
    $minY = $y - $scale / 2;

    $out_matrix = array();
    for($i = 0; $i < $resolution; $i++){
      array_push($out_matrix, range(0, $resolution));
    }
    
    for ($row = 0; $row < $resolution; $row++){
        for ($col = 0; $col < $resolution; $col++){
            $x = $minX + $col * $scale / $resolution;
            $y = $minY + $row * $scale / $resolution;
            $oldX = $x;
            $oldY = $y;
            for ($i = 0; $i < $precision + 1; $i++){
                $real = $x*$x - $y*$y; #real component of z^2
                $imag = 2 * $x * $y; #imaginary component of z^2
                $x = $real + $oldX; #real component of new z
                $y = $imag + $oldY; #imaginary component of new z
                if ($x*$x + $y*$y > 4){
                    break;
                }
            $out_matrix[$col][$row] = $i;
            }
        }
    }
    return $out_matrix;
}    
$res = 1000;

$c = $res/255;
$matrix = calc_mand($res, 100);

$gd = imagecreatetruecolor($res, $res);

for ($i = 0; $i < $res; $i++) {
  for ($j = 0; $j < $res; $j++) {
    imagesetpixel($gd, $i, $j, imagecolorallocate($gd, round($matrix[$i][$j]/$c), round(255 - $matrix[$i][$j]/$c), 255));
  }
}

header('Content-Type: image/png');
imagepng($gd, "mandelbrot.png");
?>

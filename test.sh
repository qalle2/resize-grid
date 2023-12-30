clear
rm -f test-out/*.png
echo "xxx" > test-out/existing-garbage

echo "=== Converting ==="
python3 resizegrid.py test-in/8x8-pal.png test-out/8x8-pal.png
python3 resizegrid.py test-in/8x8-rgb.png test-out/8x8-rgb.png
python3 resizegrid.py test-in/8x8-rgb.png test-out/8x8-rgb-11x13-green.png --otw 11 --oth 13 --bgcolor 00ff00
echo

echo "=== These should cause six distinct errors before files are opened ==="
python3 resizegrid.py test-in/8x8-pal.png  test-out/error1.png --otw 7
python3 resizegrid.py test-in/8x8-pal.png  test-out/error2.png --oth 7
python3 resizegrid.py test-in/8x8-pal.png  test-out/error3.png --otw 8 --oth 8
python3 resizegrid.py test-in/8x8-pal.png  test-out/error4.png --bgcolor x
python3 resizegrid.py test-in/nonexistent  test-out/error5.png
python3 resizegrid.py test-in/8x8-pal.png  test-out/existing-garbage
echo

echo "=== These should cause three distinct errors after files are opened ==="
python3 resizegrid.py test-out/existing-garbage test-out/error6.png
python3 resizegrid.py test-in/8x8-rgba.png      test-out/error7.png
python3 resizegrid.py test-in/8x8-pal.png       test-out/nonexistent/
echo

echo "=== Validate images under test-out/ manually ==="
echo

rm test-out/error*.png

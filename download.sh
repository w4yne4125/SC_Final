cd ../test;
for i in {1..1500}
do
    cd $i
    link=`head -n 1 ./${i}_link.txt`;
    echo $link;
    youtube-dl -x --audio-format wav $link -o "${i}.wav"
    cd ../
    sleep 1
done

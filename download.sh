cd ../;
for i in {41..500}
do
    cd $i
    link=`head -n 1 ./${i}_link.txt`;
    echo $link;
    youtube-dl -x --audio-format wav $link -o "${i}.wav"
    cd ../
    sleep 1
done

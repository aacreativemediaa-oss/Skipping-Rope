#!/bin/bash
set -e
M=/home/user/media; O=/home/user/hf/kesilapan/assets/media
# name src start dur
while read n src ss dur; do
  f=$M/$src
  trc=$(ffprobe -v error </dev/null -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$f")
  aidx=$(ffprobe </dev/null -v error -select_streams a -show_entries stream=index,codec_name -of csv=p=0 "$f" | grep aac | head -1 | cut -d, -f1)
  vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=60"
  if [[ "$trc" == arib-std-b67* ]]; then
    vf="zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,$vf"
  fi
  ffmpeg -nostdin -loglevel error -y -i "$f" -filter_complex "[0:v:0]trim=start=$ss:duration=$dur,setpts=PTS-STARTPTS,$vf,format=yuv420p[v];[0:$aidx]atrim=start=$ss:duration=$dur,asetpts=PTS-STARTPTS[a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 14 -g 30 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$O/$n.mp4"
  L=$(ffmpeg -nostdin -nostats -i "$O/$n.mp4" -vn -af ebur128 -f null - 2>&1 | grep " I:" | tail -1 | awk '{print $2}')
  echo "$n $src $ss $dur LUFS=$L"
done <<LIST
m1_hook IMG_1097.MOV 7.2 4.0
m2_tinggi video_20260419_202731.mp4 8.0 7.0
m3_kasut IMG_1071.MOV 7.0 6.5
m4_tali IMG_1098.MOV 4.7 5.5
m5_counter lv_0_20251026143250.mp4 26.3 3.0
m6_bola IMG_1074.MOV 2.0 3.0
m7_panjang IMG_1088b.MOV 4.2 3.0
m8_pemula IMG_0727.MOV 7.5 3.5
m9_pink copy_C56E.mov 19.5 2.8
m10_ungu copy_2AF7.mov 4.35 2.8
LIST

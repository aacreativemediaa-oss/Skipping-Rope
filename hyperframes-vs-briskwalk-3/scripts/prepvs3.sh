#!/bin/bash
set -e
M=/home/user/media; O=/home/user/hf/skippingvs3/assets/media
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
k1_hook IMG_1161.MOV 7.0 4.0
k2_cal IMG_1093.MOV 5.5 5.0
k3_cal IMG_1162.MOV 6.5 5.0
k4_otot video_20260218_150009.mp4 11.0 7.0
k5_ruang IMG_1076.MOV 1.0 5.5
k6_counter copy_2AF7.mov 41.6 3.0
k7_bola IMG_0725.MOV 1.0 3.0
k8_tali IMG_1100.MOV 5.5 3.0
k9_pemula IMG_1078.MOV 2.0 3.5
k10_cta video_20260419_202951.mp4 13.0 5.5
LIST

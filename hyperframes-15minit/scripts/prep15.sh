#!/bin/bash
set -e
M=/home/user/media; O=/home/user/hf/skipping15/assets/media
# name src start dur
while read n src ss dur; do
  f=$M/$src
  trc=$(ffprobe -v error </dev/null -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$f")
  aidx=$(ffprobe </dev/null -v error -select_streams a -show_entries stream=index,codec_name -of csv=p=0 "$f" | grep aac | head -1 | cut -d, -f1)
  vf="scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=60"
  if [ "$trc" = "arib-std-b67" ]; then
    vf="zscale=tin=arib-std-b67:min=bt2020nc:pin=bt2020:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,$vf"
  fi
  ffmpeg -nostdin -loglevel error -y -i "$f" -filter_complex "[0:v:0]trim=start=$ss:duration=$dur,setpts=PTS-STARTPTS,$vf,format=yuv420p[v];[0:$aidx]atrim=start=$ss:duration=$dur,asetpts=PTS-STARTPTS[a]" -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 14 -g 30 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart "$O/$n.mp4"
  L=$(ffmpeg -nostdin -nostats -i "$O/$n.mp4" -vn -af ebur128 -f null - 2>&1 | grep " I:" | tail -1 | awk '{print $2}')
  echo "$n $src $ss $dur LUFS=$L"
done <<LIST
d1_hook copy_9492.MOV 0.5 4.0
d2_cal IMG_1987.MOV 3.5 5.0
d3_cal video_20260419_202843.mp4 2.0 5.0
d4_otot IMG_1093.MOV 2.0 3.0
d5_otot IMG_1161.MOV 3.0 3.0
d6_counter lv_0_20251026143250.mp4 26.2 3.5
d7_rumah IMG_1073.MOV 0.5 4.0
d8_cta video_20260419_202951.mp4 5.0 5.5
d9_bola IMG_1207.MOV 2.5 3.0
d10_tali IMG_1100.MOV 1.5 3.0
LIST

#!/bin/bash
set -e
M=/home/user/media; O=/home/user/hf/proj/media
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
c1_hook video_20260419_202731.mp4 0.5 4.0
c2_cal video_20260218_150009.mp4 3.0 5.0
c3_cal IMG_1097.MOV 2.0 5.0
c4_otot IMG_1206.MOV 2.0 4.0
c5_otot IMG_1099.MOV 1.0 4.0
c6_counter copy_C56E.mov 31.3 3.5
c7_count copy_2AF7.mov 42.0 2.5
c8_rumah copy_2AF7.mov 13.0 3.5
c9_cta video_20251025_145958_edit.mp4 12.0 5.5
LIST

// alert('瞅你咋地？')

// let file_path = ["C:/爬虫战果/音乐/Donawhale - Echo.flac", "C:/爬虫战果/音乐/cry for me.mp3", "C:/爬虫战果/音乐/JORDANN - Dehors.mp3", "C:/爬虫战果/音乐/古典留声机 - 月光曲 德彪西.mp3", "C:/爬虫战果/音乐/林俊杰 - 醉赤壁.mp3", "C:/爬虫战果/音乐/周杰伦 - 红尘客栈.mp3", "C:/爬虫战果/音乐/周杰伦 - 烟花易冷.mp3", "C:/爬虫战果/音乐/周杰伦 - 稻香.mp3"]

let file_path = ["Donawhale - Echo.flac", "cry for me.mp3", "JORDANN - Dehors.mp3", "古典留声机 - 月光曲 德彪西.mp3", "林俊杰 - 醉赤壁.mp3", "周杰伦 - 红尘客栈.mp3", "周杰伦 - 烟花易冷.mp3", "周杰伦 - 稻香.mp3"]

for (let i = 1; i <= 8; i++) {
    let index = Math.floor(Math.random() * file_path.length)
    let random_path = file_path[index]
    file_path.splice(index, 1)
    let music_src = document.querySelector(`td#t${i}`).querySelector('audio')
    fetch(`/get_music_url?filename=${random_path}`)
        .then(response => response.json())
        .then(data => {
            let music_url = data.url
            music_src.setAttribute('src', music_url)
        })
        .catch(error => {
            console.error('Error fetching music URL:', error)
        })
    let music_text = document.querySelector(`th#t${i}`)
    // random_text = random_path.match('.*(?:/| - )(.*?)(?:.mp3|.flac)')
    random_text = random_path.match('.*(?: - )(.*?)(?:.mp3|.flac)|(.*?)((?:.mp3|.flac))')
    // random_text = random_path.match('(.*?)((?:.mp3|.flac))|.*(?: - )(.*?)(?:.mp3|.flac)')[1]
    if (random_text[1] == undefined) {
        random_text = random_text[2]
    } else {
        random_text = random_text[1]
    }
    music_text.innerHTML = random_text
}
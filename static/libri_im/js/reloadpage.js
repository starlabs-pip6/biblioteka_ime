function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

function reloadpage(id) {
    await sleep(1200)
    // document.getElementById('id_body').value='';
    location.reload();
    return false;
}

function commentReplyToggle(parent_id) {
  console.log(parent_id)
}
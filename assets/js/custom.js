
document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.getElementById('loadinggif-part').style.opacity = '1';
        setTimeout( () => {
            document.getElementById('loadinggif-part').style.display = 'block';
        }, 500)
    } else {
        document.getElementById('loadinggif-part').style.opacity = '0';
        setTimeout( () => {
            document.getElementById('loadinggif-part').style.display = 'none';
        }, 500)
    }
};

// persian digit
$(document).ready(function(){
    $('.digit').persiaNumber();
});

// open sidebar
open_sidebar=() => {
    $('section.quick-navbar div').css({'transform': 'translateX(0)'});
    setTimeout( () => {
        $('aside').hide();
        $('article').hide();
        $('section.top-div-navbar').hide();
    }, 800) 
}
close_sidebar=() => {
    $('section.quick-navbar div').css({'transform': 'translateX(3000px)'});
    $('aside').show();
    $('article').show();
    $('section.top-div-navbar').show();
}

// open and close the modal
openModal = (modalID) => { 
    $('#' + modalID).css({'display':'block'});
    setTimeout( () => {
        $('#' + modalID + ' .bg-img-wrapper').css({'opacity': '1'})
    }, 200) 
    setTimeout( () => {
        $('#' + modalID + ' .modal-content').css({'transform': 'translateY(0)'}); 
    }, 600) 
    $('aside').hide();
    $('section.top-div-navbar').hide();
}
closeModal = (modalID) => { 
    setTimeout( () => {
        $('#' + modalID + ' .modal-content').css({'transform': 'translateY(-500px)'}); 
    }, 200)
    setTimeout( () => {
        $('#' + modalID + ' .bg-img-wrapper').css({'opacity': '0'})
    }, 400) 
    setTimeout( () => {
        $('#' + modalID).css({'display':'none'});
    }, 600) 
    $('aside').show();
    $('section.top-div-navbar').show();
}

// open and close forms
open_form = () => {
    $('div#form-div-wrapper').css({'display':'block'})
    setTimeout( () => {
        $('form#form-add').css({'opacity':'1'})
    }, 500)
    $('p#open-parg').css({'display':'none'})
    $('p#close-parg').css({'display':'block'})
}
close_form = () => {
    $('form#form-add').css({'opacity':'0'})
    setTimeout( () => {
        $('div#form-div-wrapper').css({'display':'none'})
    }, 500)
    $('p#open-parg').css({'display':'block'})
    $('p#close-parg').css({'display':'none'})
}

// close msg box 
close_msg = (number) => {
    document.getElementsByClassName('msg-msgs')[number-1].style.animation = 'fadeOut 1s forwards';
}

function copy_text(textCp, divId) {
    const el = document.createElement('textarea');
    el.value = textCp;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    document.getElementById(divId).innerText = 'Copied';
    setTimeout( ()=> {
        document.getElementById(divId).innerText = textCp;
    }, 5000)
}
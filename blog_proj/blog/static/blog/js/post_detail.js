    function getcookie(name){
        let cookieval=null;

        const cookies=document.cookie.split(";")

        for(let cookie of cookies){
            cookie=cookie.trim();
            //removes the sapces in stringformat

            if(cookie.startsWith(name+"=")){
                cookieval=cookie.substring(name.length+1);
            }
        }

        return cookieval;
    }


    function likesPost(postid){
        const csrftoken=getcookie("csrftoken")

        fetch(`/post/${postid}/like_post/`,{
            method:"POST",
            headers:{
                "X-CSRFToken":csrftoken
            }
        })
        .then(response=>response.json())
        .then(data=>{
            document.getElementById(`likes-${postid}`).innerText=data.likes;
            
        });
    }

    function addComment(postid){

        const csrftoken=getcookie("csrftoken");
        const comment=document.getElementById("comment-text").value;
        fetch(`/post/${postid}/comment/`,{
            method:"POST",
            headers:{
                "X-CSRFToken":csrftoken,
                "Content-Type":"application/json"

            },
            body:JSON.stringify({
                comment:comment
            })
        })

        .then(response=>response.json())
        .then(
            data=>{
                const comments=document.getElementById("comments");
                    comments.innerHTML+=`
                    <p><strong>${data.writer}
                    </strong><br>
                    ${data.comment}
                    </p>`;
                      }
        )
        document.getElementById("comment-text").value='';

    }

    function like_comment(post_id,comment_id){
        const csrftoken=getcookie("csrftoken")
        fetch(`/post/${post_id}/commentlike/${comment_id}`,
        {method:"POST",
        headers:{
            "X-CSRFToken":csrftoken,
        }
    }
        )
        .then(response=>response.json())
        .then(data=>{
        document.getElementById(`likeit-${comment_id}`).innerText=data.likes;
    })
}

    function edit_comment(post_id,comment_id){
        
        
        const paragraph=document.getElementById(`comment-${comment_id}`)
        const textarea=document.createElement("textarea");
        textarea.value=paragraph.innerText;

        paragraph.replaceWith(textarea)
        const edit=document.getElementById(`editbutton-${comment_id}`)

        const savebutton=document.createElement("button");
        savebutton.innerText="Save";
        
    
        savebutton.onclick = function () {
            save_comment(post_id, comment_id);
        };

        edit.replaceWith(savebutton);
        savebutton.id = `savebutton-${comment_id}`;

        textarea.id = `commenttext-${comment_id}`;
    }

    function save_comment(post_id,comment_id){

        const csrftoken=getcookie("csrftoken");
        const textarea=document.getElementById(`commenttext-${comment_id}`)



        fetch(`/post/${post_id}/editcomment/${comment_id}`,
        {method:"POST",
        headers:{
            "X-CSRFToken":csrftoken,
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            comment:textarea.value
        })


    }
    )   .then(response=>response.json())
        .then(data=>{
        const paragraph = document.createElement("p");
        paragraph.innerText = data.comment;
        paragraph.id = `comment-${comment_id}`
        textarea.replaceWith(paragraph);
        const editButton = document.createElement("button");
        editButton.innerText = "Edit";
        editButton.id = `editbutton-${comment_id}`;

        editButton.onclick = function () {
            edit_comment(post_id, comment_id);
};
const savebutton = document.getElementById(`savebutton-${comment_id}`);
savebutton.replaceWith(editButton);

    })

    }


    function delete_comment(post_id,comment_id){

        const csrftoken=getcookie("csrftoken");
        fetch(`/post/${post_id}/deletecomment/${comment_id}`,
        {method:"POST",
            headers:{
            "X-CSRFToken":csrftoken,
        }}
        )
        .then(response=>{
            if(!response.ok){
                throw new Error("Could not delete comment!");
            }
            return response.json();
        })
        .then(data=>{
            if(data.success){
                document.getElementById(`comment-container-${comment_id}`)
                .remove()
            }
        })
        .catch(error=>{
            console.error(error);
        })
        }


        


    
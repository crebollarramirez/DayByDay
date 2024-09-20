import react, {useState} from "react"


function NewTaskForm(){
    const [content, setContent] = useState("")

    const handleSubmit = async (e) => {
        e.preventDefault();

        try{
            const res = await api.post((route, {content}));
        }catch(err){
            alert(err)
        }finally{
            console.log("The task was created and everything is working good")
        }
    };

    return (
        <form onSubmit={handleSubmit} className="form-container">
            <h1>Submit a Task</h1>
            <input className="form-input" type="text" value={content} onChange={(e) => setContent(e.target.value)} placeholder="Content"/>
            <button className="form-button" type="submit">
                Submit
            </button>
        </form>
    )
}
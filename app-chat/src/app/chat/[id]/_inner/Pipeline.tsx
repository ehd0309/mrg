import { Divider } from "@nextui-org/react";
import Image from "next/image";

interface PipelineProps {
    pre_process_image: string | null;
    post_process_image: string | null;
}

const Pipeline = ({ pre_process_image, post_process_image }: PipelineProps) => {
    return <div className="flex mt-2 gap-4">
        <div>
        <p className="font-semibold text-center">Data Preparation</p>
        <Divider className="m-2"/>
        {pre_process_image && <Image src={pre_process_image} width={200} height={328} alt="pre-image"/>}
        </div>
        <div className="flex items-center font-bold text-xl">
            {"→"}
        </div>
        <div>
        <p className="font-semibold text-center">Question-Answer</p>
        <Divider className="m-2"/>
        {post_process_image && <Image src={post_process_image} width={200} height={328} alt="post-image"/>}
        </div>
    </div>
}

export default Pipeline;
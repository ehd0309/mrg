import Image from "next/image";
import Link from "next/link";

const Header = () => {
  return (
    <div className="bg-black py-2 text-white">
      <div className="flex justify-between items-center m-auto px-10">
        <h1 className="font-bold">RAG-LLM CHAT</h1>
        <div className="flex items-center">
          <Link href="https://github.com/ehd0309/mrg">
            <Image
              src="/images/github.svg"
              width={36}
              height={36}
              alt="github"
            />
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Header;

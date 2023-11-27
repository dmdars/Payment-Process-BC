import { useState } from "react";

interface Props {
	csName?: string;
}

const TopLogo = ({csName}:Props) => {

	const [cssName, setCssName] = useState("h1 text-center");
	csName && setCssName(csName);

	return (
		<>
			<div className={cssName}> 
				<p>
					Big Logo
				</p>
			</div>
		</>
	)
};

export default TopLogo;
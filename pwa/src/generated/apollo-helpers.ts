import { FieldPolicy, FieldReadFunction, TypePolicies } from '@apollo/client/cache';
export type QueryKeySpecifier = ('currentUser' | 'waffle' | 'activeSituation' | 'getIrnEntity' | 'space' | 'getSpaces' | 'item' | 'items' | 'suggestType' | 'entitySearch' | QueryKeySpecifier)[];
export type QueryFieldPolicy = {
	currentUser?: FieldPolicy<any> | FieldReadFunction<any>,
	waffle?: FieldPolicy<any> | FieldReadFunction<any>,
	activeSituation?: FieldPolicy<any> | FieldReadFunction<any>,
	getIrnEntity?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	getSpaces?: FieldPolicy<any> | FieldReadFunction<any>,
	item?: FieldPolicy<any> | FieldReadFunction<any>,
	items?: FieldPolicy<any> | FieldReadFunction<any>,
	suggestType?: FieldPolicy<any> | FieldReadFunction<any>,
	entitySearch?: FieldPolicy<any> | FieldReadFunction<any>
};
export type UserKeySpecifier = ('id' | 'username' | 'firstName' | 'lastName' | 'email' | 'isStaff' | 'isActive' | 'groups' | 'userPermissions' | 'allPermissions' | 'groupPermissions' | UserKeySpecifier)[];
export type UserFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	username?: FieldPolicy<any> | FieldReadFunction<any>,
	firstName?: FieldPolicy<any> | FieldReadFunction<any>,
	lastName?: FieldPolicy<any> | FieldReadFunction<any>,
	email?: FieldPolicy<any> | FieldReadFunction<any>,
	isStaff?: FieldPolicy<any> | FieldReadFunction<any>,
	isActive?: FieldPolicy<any> | FieldReadFunction<any>,
	groups?: FieldPolicy<any> | FieldReadFunction<any>,
	userPermissions?: FieldPolicy<any> | FieldReadFunction<any>,
	allPermissions?: FieldPolicy<any> | FieldReadFunction<any>,
	groupPermissions?: FieldPolicy<any> | FieldReadFunction<any>
};
export type NodeKeySpecifier = ('id' | NodeKeySpecifier)[];
export type NodeFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>
};
export type GroupKeySpecifier = ('id' | 'name' | 'permissions' | GroupKeySpecifier)[];
export type GroupFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	permissions?: FieldPolicy<any> | FieldReadFunction<any>
};
export type PermissionKeySpecifier = ('id' | 'name' | 'contentType' | 'codename' | PermissionKeySpecifier)[];
export type PermissionFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	contentType?: FieldPolicy<any> | FieldReadFunction<any>,
	codename?: FieldPolicy<any> | FieldReadFunction<any>
};
export type WaffleKeySpecifier = ('flags' | 'switches' | 'samples' | 'all' | 'flag' | 'switch' | 'sample' | 'flagDefault' | 'switchDefault' | 'sampleDefault' | WaffleKeySpecifier)[];
export type WaffleFieldPolicy = {
	flags?: FieldPolicy<any> | FieldReadFunction<any>,
	switches?: FieldPolicy<any> | FieldReadFunction<any>,
	samples?: FieldPolicy<any> | FieldReadFunction<any>,
	all?: FieldPolicy<any> | FieldReadFunction<any>,
	flag?: FieldPolicy<any> | FieldReadFunction<any>,
	switch?: FieldPolicy<any> | FieldReadFunction<any>,
	sample?: FieldPolicy<any> | FieldReadFunction<any>,
	flagDefault?: FieldPolicy<any> | FieldReadFunction<any>,
	switchDefault?: FieldPolicy<any> | FieldReadFunction<any>,
	sampleDefault?: FieldPolicy<any> | FieldReadFunction<any>
};
export type WaffleFlagKeySpecifier = ('id' | 'name' | 'active' | 'note' | 'created' | 'modified' | WaffleFlagKeySpecifier)[];
export type WaffleFlagFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	active?: FieldPolicy<any> | FieldReadFunction<any>,
	note?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>
};
export type WaffleItemKeySpecifier = ('id' | 'name' | 'active' | 'note' | WaffleItemKeySpecifier)[];
export type WaffleItemFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	active?: FieldPolicy<any> | FieldReadFunction<any>,
	note?: FieldPolicy<any> | FieldReadFunction<any>
};
export type TimeStampedKeySpecifier = ('created' | 'modified' | TimeStampedKeySpecifier)[];
export type TimeStampedFieldPolicy = {
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>
};
export type WaffleSwitchKeySpecifier = ('id' | 'name' | 'active' | 'note' | 'created' | 'modified' | WaffleSwitchKeySpecifier)[];
export type WaffleSwitchFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	active?: FieldPolicy<any> | FieldReadFunction<any>,
	note?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>
};
export type WaffleSampleKeySpecifier = ('id' | 'name' | 'active' | 'note' | 'created' | 'modified' | WaffleSampleKeySpecifier)[];
export type WaffleSampleFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	active?: FieldPolicy<any> | FieldReadFunction<any>,
	note?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SituationKeySpecifier = ('id' | 'created' | 'modified' | 'user' | 'spaces' | 'items' | 'state' | 'exitCondition' | SituationKeySpecifier)[];
export type SituationFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	user?: FieldPolicy<any> | FieldReadFunction<any>,
	spaces?: FieldPolicy<any> | FieldReadFunction<any>,
	items?: FieldPolicy<any> | FieldReadFunction<any>,
	state?: FieldPolicy<any> | FieldReadFunction<any>,
	exitCondition?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SpaceNodeKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'parent' | 'parents' | 'children' | 'isLeaf' | 'isChild' | 'isRoot' | 'items' | 'data' | 'itemCount' | 'layout' | 'dimensions' | 'volume' | 'gridScale' | 'gridConfig' | SpaceNodeKeySpecifier)[];
export type SpaceNodeFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	parent?: FieldPolicy<any> | FieldReadFunction<any>,
	parents?: FieldPolicy<any> | FieldReadFunction<any>,
	children?: FieldPolicy<any> | FieldReadFunction<any>,
	isLeaf?: FieldPolicy<any> | FieldReadFunction<any>,
	isChild?: FieldPolicy<any> | FieldReadFunction<any>,
	isRoot?: FieldPolicy<any> | FieldReadFunction<any>,
	items?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	itemCount?: FieldPolicy<any> | FieldReadFunction<any>,
	layout?: FieldPolicy<any> | FieldReadFunction<any>,
	dimensions?: FieldPolicy<any> | FieldReadFunction<any>,
	volume?: FieldPolicy<any> | FieldReadFunction<any>,
	gridScale?: FieldPolicy<any> | FieldReadFunction<any>,
	gridConfig?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SpaceInterfaceKeySpecifier = ('id' | 'name' | 'parent' | 'parents' | 'children' | 'isLeaf' | 'isChild' | 'isRoot' | 'items' | 'data' | 'itemCount' | 'layout' | 'dimensions' | 'volume' | 'gridScale' | 'gridConfig' | SpaceInterfaceKeySpecifier)[];
export type SpaceInterfaceFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	parent?: FieldPolicy<any> | FieldReadFunction<any>,
	parents?: FieldPolicy<any> | FieldReadFunction<any>,
	children?: FieldPolicy<any> | FieldReadFunction<any>,
	isLeaf?: FieldPolicy<any> | FieldReadFunction<any>,
	isChild?: FieldPolicy<any> | FieldReadFunction<any>,
	isRoot?: FieldPolicy<any> | FieldReadFunction<any>,
	items?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	itemCount?: FieldPolicy<any> | FieldReadFunction<any>,
	layout?: FieldPolicy<any> | FieldReadFunction<any>,
	dimensions?: FieldPolicy<any> | FieldReadFunction<any>,
	volume?: FieldPolicy<any> | FieldReadFunction<any>,
	gridScale?: FieldPolicy<any> | FieldReadFunction<any>,
	gridConfig?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ConnectionKeySpecifier = ('pageInfo' | 'edges' | ConnectionKeySpecifier)[];
export type ConnectionFieldPolicy = {
	pageInfo?: FieldPolicy<any> | FieldReadFunction<any>,
	edges?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ListPageInfoKeySpecifier = ('pageInfo' | ListPageInfoKeySpecifier)[];
export type ListPageInfoFieldPolicy = {
	pageInfo?: FieldPolicy<any> | FieldReadFunction<any>
};
export type PageInfoKeySpecifier = ('hasNextPage' | 'hasPreviousPage' | 'startCursor' | 'endCursor' | 'count' | PageInfoKeySpecifier)[];
export type PageInfoFieldPolicy = {
	hasNextPage?: FieldPolicy<any> | FieldReadFunction<any>,
	hasPreviousPage?: FieldPolicy<any> | FieldReadFunction<any>,
	startCursor?: FieldPolicy<any> | FieldReadFunction<any>,
	endCursor?: FieldPolicy<any> | FieldReadFunction<any>,
	count?: FieldPolicy<any> | FieldReadFunction<any>
};
export type EdgeKeySpecifier = ('cursor' | 'node' | EdgeKeySpecifier)[];
export type EdgeFieldPolicy = {
	cursor?: FieldPolicy<any> | FieldReadFunction<any>,
	node?: FieldPolicy<any> | FieldReadFunction<any>
};
export type LayoutKeySpecifier = ('x' | 'y' | 'w' | 'h' | LayoutKeySpecifier)[];
export type LayoutFieldPolicy = {
	x?: FieldPolicy<any> | FieldReadFunction<any>,
	y?: FieldPolicy<any> | FieldReadFunction<any>,
	w?: FieldPolicy<any> | FieldReadFunction<any>,
	h?: FieldPolicy<any> | FieldReadFunction<any>
};
export type DimensionsKeySpecifier = ('x' | 'y' | 'z' | DimensionsKeySpecifier)[];
export type DimensionsFieldPolicy = {
	x?: FieldPolicy<any> | FieldReadFunction<any>,
	y?: FieldPolicy<any> | FieldReadFunction<any>,
	z?: FieldPolicy<any> | FieldReadFunction<any>
};
export type GridLayoutConfigKeySpecifier = ('cols' | 'rowBasis' | GridLayoutConfigKeySpecifier)[];
export type GridLayoutConfigFieldPolicy = {
	cols?: FieldPolicy<any> | FieldReadFunction<any>,
	rowBasis?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ProtocolKeySpecifier = ('irn' | 'qr' | ProtocolKeySpecifier)[];
export type ProtocolFieldPolicy = {
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>
};
export type GridSpaceNodeKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'parent' | 'parents' | 'children' | 'isLeaf' | 'isChild' | 'isRoot' | 'items' | 'data' | 'itemCount' | 'layout' | 'dimensions' | 'volume' | 'gridScale' | 'gridConfig' | 'gridSize' | GridSpaceNodeKeySpecifier)[];
export type GridSpaceNodeFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	parent?: FieldPolicy<any> | FieldReadFunction<any>,
	parents?: FieldPolicy<any> | FieldReadFunction<any>,
	children?: FieldPolicy<any> | FieldReadFunction<any>,
	isLeaf?: FieldPolicy<any> | FieldReadFunction<any>,
	isChild?: FieldPolicy<any> | FieldReadFunction<any>,
	isRoot?: FieldPolicy<any> | FieldReadFunction<any>,
	items?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	itemCount?: FieldPolicy<any> | FieldReadFunction<any>,
	layout?: FieldPolicy<any> | FieldReadFunction<any>,
	dimensions?: FieldPolicy<any> | FieldReadFunction<any>,
	volume?: FieldPolicy<any> | FieldReadFunction<any>,
	gridScale?: FieldPolicy<any> | FieldReadFunction<any>,
	gridConfig?: FieldPolicy<any> | FieldReadFunction<any>,
	gridSize?: FieldPolicy<any> | FieldReadFunction<any>
};
export type GridSizeKeySpecifier = ('cols' | 'rows' | GridSizeKeySpecifier)[];
export type GridSizeFieldPolicy = {
	cols?: FieldPolicy<any> | FieldReadFunction<any>,
	rows?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ItemKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'data' | 'space' | 'spaceParents' | ItemKeySpecifier)[];
export type ItemFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	spaceParents?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ItemInterfaceKeySpecifier = ('id' | 'name' | 'data' | 'space' | 'spaceParents' | ItemInterfaceKeySpecifier)[];
export type ItemInterfaceFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	spaceParents?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ToolKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'data' | 'space' | 'spaceParents' | ToolKeySpecifier)[];
export type ToolFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	spaceParents?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ConsumableKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'data' | 'space' | 'spaceParents' | 'count' | 'warningEnabled' | 'warningCount' | 'warning' | ConsumableKeySpecifier)[];
export type ConsumableFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	spaceParents?: FieldPolicy<any> | FieldReadFunction<any>,
	count?: FieldPolicy<any> | FieldReadFunction<any>,
	warningEnabled?: FieldPolicy<any> | FieldReadFunction<any>,
	warningCount?: FieldPolicy<any> | FieldReadFunction<any>,
	warning?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ConsumableInterfaceKeySpecifier = ('count' | 'warningEnabled' | 'warningCount' | 'warning' | ConsumableInterfaceKeySpecifier)[];
export type ConsumableInterfaceFieldPolicy = {
	count?: FieldPolicy<any> | FieldReadFunction<any>,
	warningEnabled?: FieldPolicy<any> | FieldReadFunction<any>,
	warningCount?: FieldPolicy<any> | FieldReadFunction<any>,
	warning?: FieldPolicy<any> | FieldReadFunction<any>
};
export type TrackedConsumableKeySpecifier = ('id' | 'created' | 'modified' | 'irn' | 'qr' | 'name' | 'data' | 'space' | 'spaceParents' | 'count' | 'warningEnabled' | 'warningCount' | 'warning' | TrackedConsumableKeySpecifier)[];
export type TrackedConsumableFieldPolicy = {
	id?: FieldPolicy<any> | FieldReadFunction<any>,
	created?: FieldPolicy<any> | FieldReadFunction<any>,
	modified?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	qr?: FieldPolicy<any> | FieldReadFunction<any>,
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	data?: FieldPolicy<any> | FieldReadFunction<any>,
	space?: FieldPolicy<any> | FieldReadFunction<any>,
	spaceParents?: FieldPolicy<any> | FieldReadFunction<any>,
	count?: FieldPolicy<any> | FieldReadFunction<any>,
	warningEnabled?: FieldPolicy<any> | FieldReadFunction<any>,
	warningCount?: FieldPolicy<any> | FieldReadFunction<any>,
	warning?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SearchResultKeySpecifier = ('score' | 'irn' | 'object' | SearchResultKeySpecifier)[];
export type SearchResultFieldPolicy = {
	score?: FieldPolicy<any> | FieldReadFunction<any>,
	irn?: FieldPolicy<any> | FieldReadFunction<any>,
	object?: FieldPolicy<any> | FieldReadFunction<any>
};
export type MutationKeySpecifier = ('root' | 'selectEntities' | 'unselectEntities' | 'abandonSituation' | 'addSpace' | 'addGridSpace' | 'updateSpace' | 'updateGridSpace' | 'updateSpaceLayout' | 'removeSpace' | 'addItem' | 'addTool' | 'addConsumable' | 'updateItem' | 'updateTool' | 'updateConsumable' | 'deleteItem' | 'moveItem' | 'removeItem' | MutationKeySpecifier)[];
export type MutationFieldPolicy = {
	root?: FieldPolicy<any> | FieldReadFunction<any>,
	selectEntities?: FieldPolicy<any> | FieldReadFunction<any>,
	unselectEntities?: FieldPolicy<any> | FieldReadFunction<any>,
	abandonSituation?: FieldPolicy<any> | FieldReadFunction<any>,
	addSpace?: FieldPolicy<any> | FieldReadFunction<any>,
	addGridSpace?: FieldPolicy<any> | FieldReadFunction<any>,
	updateSpace?: FieldPolicy<any> | FieldReadFunction<any>,
	updateGridSpace?: FieldPolicy<any> | FieldReadFunction<any>,
	updateSpaceLayout?: FieldPolicy<any> | FieldReadFunction<any>,
	removeSpace?: FieldPolicy<any> | FieldReadFunction<any>,
	addItem?: FieldPolicy<any> | FieldReadFunction<any>,
	addTool?: FieldPolicy<any> | FieldReadFunction<any>,
	addConsumable?: FieldPolicy<any> | FieldReadFunction<any>,
	updateItem?: FieldPolicy<any> | FieldReadFunction<any>,
	updateTool?: FieldPolicy<any> | FieldReadFunction<any>,
	updateConsumable?: FieldPolicy<any> | FieldReadFunction<any>,
	deleteItem?: FieldPolicy<any> | FieldReadFunction<any>,
	moveItem?: FieldPolicy<any> | FieldReadFunction<any>,
	removeItem?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SituationPayloadKeySpecifier = ('success' | 'object' | 'entities' | SituationPayloadKeySpecifier)[];
export type SituationPayloadFieldPolicy = {
	success?: FieldPolicy<any> | FieldReadFunction<any>,
	object?: FieldPolicy<any> | FieldReadFunction<any>,
	entities?: FieldPolicy<any> | FieldReadFunction<any>
};
export type SpacePayloadKeySpecifier = ('success' | 'errors' | 'object' | SpacePayloadKeySpecifier)[];
export type SpacePayloadFieldPolicy = {
	success?: FieldPolicy<any> | FieldReadFunction<any>,
	errors?: FieldPolicy<any> | FieldReadFunction<any>,
	object?: FieldPolicy<any> | FieldReadFunction<any>
};
export type PayloadKeySpecifier = ('success' | 'errors' | PayloadKeySpecifier)[];
export type PayloadFieldPolicy = {
	success?: FieldPolicy<any> | FieldReadFunction<any>,
	errors?: FieldPolicy<any> | FieldReadFunction<any>
};
export type FieldErrorKeySpecifier = ('name' | 'values' | FieldErrorKeySpecifier)[];
export type FieldErrorFieldPolicy = {
	name?: FieldPolicy<any> | FieldReadFunction<any>,
	values?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ErrorDetailKeySpecifier = ('error' | 'code' | ErrorDetailKeySpecifier)[];
export type ErrorDetailFieldPolicy = {
	error?: FieldPolicy<any> | FieldReadFunction<any>,
	code?: FieldPolicy<any> | FieldReadFunction<any>
};
export type ItemPayloadKeySpecifier = ('success' | 'errors' | 'object' | ItemPayloadKeySpecifier)[];
export type ItemPayloadFieldPolicy = {
	success?: FieldPolicy<any> | FieldReadFunction<any>,
	errors?: FieldPolicy<any> | FieldReadFunction<any>,
	object?: FieldPolicy<any> | FieldReadFunction<any>
};
export type TypedTypePolicies = TypePolicies & {
	Query?: {
		keyFields?: false | QueryKeySpecifier | (() => undefined | QueryKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: QueryFieldPolicy,
	},
	User?: {
		keyFields?: false | UserKeySpecifier | (() => undefined | UserKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: UserFieldPolicy,
	},
	Node?: {
		keyFields?: false | NodeKeySpecifier | (() => undefined | NodeKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: NodeFieldPolicy,
	},
	Group?: {
		keyFields?: false | GroupKeySpecifier | (() => undefined | GroupKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: GroupFieldPolicy,
	},
	Permission?: {
		keyFields?: false | PermissionKeySpecifier | (() => undefined | PermissionKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: PermissionFieldPolicy,
	},
	Waffle?: {
		keyFields?: false | WaffleKeySpecifier | (() => undefined | WaffleKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: WaffleFieldPolicy,
	},
	WaffleFlag?: {
		keyFields?: false | WaffleFlagKeySpecifier | (() => undefined | WaffleFlagKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: WaffleFlagFieldPolicy,
	},
	WaffleItem?: {
		keyFields?: false | WaffleItemKeySpecifier | (() => undefined | WaffleItemKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: WaffleItemFieldPolicy,
	},
	TimeStamped?: {
		keyFields?: false | TimeStampedKeySpecifier | (() => undefined | TimeStampedKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: TimeStampedFieldPolicy,
	},
	WaffleSwitch?: {
		keyFields?: false | WaffleSwitchKeySpecifier | (() => undefined | WaffleSwitchKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: WaffleSwitchFieldPolicy,
	},
	WaffleSample?: {
		keyFields?: false | WaffleSampleKeySpecifier | (() => undefined | WaffleSampleKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: WaffleSampleFieldPolicy,
	},
	Situation?: {
		keyFields?: false | SituationKeySpecifier | (() => undefined | SituationKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SituationFieldPolicy,
	},
	SpaceNode?: {
		keyFields?: false | SpaceNodeKeySpecifier | (() => undefined | SpaceNodeKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SpaceNodeFieldPolicy,
	},
	SpaceInterface?: {
		keyFields?: false | SpaceInterfaceKeySpecifier | (() => undefined | SpaceInterfaceKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SpaceInterfaceFieldPolicy,
	},
	Connection?: {
		keyFields?: false | ConnectionKeySpecifier | (() => undefined | ConnectionKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ConnectionFieldPolicy,
	},
	ListPageInfo?: {
		keyFields?: false | ListPageInfoKeySpecifier | (() => undefined | ListPageInfoKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ListPageInfoFieldPolicy,
	},
	PageInfo?: {
		keyFields?: false | PageInfoKeySpecifier | (() => undefined | PageInfoKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: PageInfoFieldPolicy,
	},
	Edge?: {
		keyFields?: false | EdgeKeySpecifier | (() => undefined | EdgeKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: EdgeFieldPolicy,
	},
	Layout?: {
		keyFields?: false | LayoutKeySpecifier | (() => undefined | LayoutKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: LayoutFieldPolicy,
	},
	Dimensions?: {
		keyFields?: false | DimensionsKeySpecifier | (() => undefined | DimensionsKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: DimensionsFieldPolicy,
	},
	GridLayoutConfig?: {
		keyFields?: false | GridLayoutConfigKeySpecifier | (() => undefined | GridLayoutConfigKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: GridLayoutConfigFieldPolicy,
	},
	Protocol?: {
		keyFields?: false | ProtocolKeySpecifier | (() => undefined | ProtocolKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ProtocolFieldPolicy,
	},
	GridSpaceNode?: {
		keyFields?: false | GridSpaceNodeKeySpecifier | (() => undefined | GridSpaceNodeKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: GridSpaceNodeFieldPolicy,
	},
	GridSize?: {
		keyFields?: false | GridSizeKeySpecifier | (() => undefined | GridSizeKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: GridSizeFieldPolicy,
	},
	Item?: {
		keyFields?: false | ItemKeySpecifier | (() => undefined | ItemKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ItemFieldPolicy,
	},
	ItemInterface?: {
		keyFields?: false | ItemInterfaceKeySpecifier | (() => undefined | ItemInterfaceKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ItemInterfaceFieldPolicy,
	},
	Tool?: {
		keyFields?: false | ToolKeySpecifier | (() => undefined | ToolKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ToolFieldPolicy,
	},
	Consumable?: {
		keyFields?: false | ConsumableKeySpecifier | (() => undefined | ConsumableKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ConsumableFieldPolicy,
	},
	ConsumableInterface?: {
		keyFields?: false | ConsumableInterfaceKeySpecifier | (() => undefined | ConsumableInterfaceKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ConsumableInterfaceFieldPolicy,
	},
	TrackedConsumable?: {
		keyFields?: false | TrackedConsumableKeySpecifier | (() => undefined | TrackedConsumableKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: TrackedConsumableFieldPolicy,
	},
	SearchResult?: {
		keyFields?: false | SearchResultKeySpecifier | (() => undefined | SearchResultKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SearchResultFieldPolicy,
	},
	Mutation?: {
		keyFields?: false | MutationKeySpecifier | (() => undefined | MutationKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: MutationFieldPolicy,
	},
	SituationPayload?: {
		keyFields?: false | SituationPayloadKeySpecifier | (() => undefined | SituationPayloadKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SituationPayloadFieldPolicy,
	},
	SpacePayload?: {
		keyFields?: false | SpacePayloadKeySpecifier | (() => undefined | SpacePayloadKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: SpacePayloadFieldPolicy,
	},
	Payload?: {
		keyFields?: false | PayloadKeySpecifier | (() => undefined | PayloadKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: PayloadFieldPolicy,
	},
	FieldError?: {
		keyFields?: false | FieldErrorKeySpecifier | (() => undefined | FieldErrorKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: FieldErrorFieldPolicy,
	},
	ErrorDetail?: {
		keyFields?: false | ErrorDetailKeySpecifier | (() => undefined | ErrorDetailKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ErrorDetailFieldPolicy,
	},
	ItemPayload?: {
		keyFields?: false | ItemPayloadKeySpecifier | (() => undefined | ItemPayloadKeySpecifier),
		queryType?: true,
		mutationType?: true,
		subscriptionType?: true,
		fields?: ItemPayloadFieldPolicy,
	}
};